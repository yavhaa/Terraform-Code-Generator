

# Provider Configuration
provider "azurerm" {
  features {}
  subscription_id = "SUBSCRIPTION_ID"
  client_id       = "CLIENT_ID"
  client_secret   = "CLIENT_SECRET"
  tenant_id       = "TENANT_ID"
  version         = "~> 2.0"
  region          = "South Central US"
}

# VPC Creation
resource "azurerm_virtual_network" "WebAppVnet" {
  name                = "WebAppVnet"
  address_space       = ["16.0.0.0/16"]
  location            = "South Central US"
  resource_group_name = "WebAppResourceGroup"
}

# Subnet Creation
resource "azurerm_subnet" "mysubnet" {
  name                 = "mysubnet"
  resource_group_name  = "WebAppResourceGroup"
  virtual_network_name = azurerm_virtual_network.WebAppVnet.name
  address_prefix       = "16.0.1.0/24"
  location             = "South Central US"
  service_endpoints    = ["Microsoft.Sql"]
  delegation {
    name = "SqlDelegation"
    service_delegation {
      name    = "Microsoft.Sql/servers"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# Internet Gateway Creation
resource "azurerm_virtual_network_gateway" "WebAppVnet_igw" {
  name                = "WebAppVnet_igw"
  location            = "South Central US"
  resource_group_name = "WebAppResourceGroup"
  type                = "IPForwarder"
  depends_on          = [azurerm_subnet.mysubnet]
}

# Route Table Creation
resource "azurerm_route_table" "WebAppVnet_route_table" {
  name                = "WebAppVnet_route_table"
  location            = "South Central US"
  resource_group_name = "WebAppResourceGroup"
  disable_bgp_route_propagation = true
  route {
    name                   = "default"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualNetworkGateway"
    next_hop_in_ip_address = azurerm_virtual_network_gateway.WebAppVnet_igw.ip_configuration[0].private_ip_address
  }
}

# Route Table Association
resource "azurerm_subnet_route_table_association" "WebAppVnet_route_table_association" {
  subnet_id      = azurerm_subnet.mysubnet.id
  route_table_id = azurerm_route_table.WebAppVnet_route_table.id
}

# Security Group Creation
resource "azurerm_network_security_group" "Alpha" {
  name                = "Alpha"
  location            = "South Central US"
  resource_group_name = "WebAppResourceGroup"
  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "AllowAllOutbound"
    priority                   = 200
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Instance Creation
resource "azurerm_virtual_machine" "WebAppDeployment" {
  name                  = "WebAppDeployment"
  location              = "South Central US"
  resource_group_name   = "WebAppResourceGroup"
  network_interface_ids = [azurerm_network_interface.WebAppDeployment_nic.id]
  vm_size               = "Standard_A2_v2"
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  os_disk {
    name              = "WebAppDeployment_osdisk"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "WebAppDeployment"
    admin_username = "adminuser"
    admin_password = "P@ssw0rd1234!"
  }
  tags = {
    Name = "WebAppDeployment"
  }
}

# Storage Account Creation
resource "azurerm_storage_account" "my_account" {
  name                     = "my_account"
  resource_group_name      = "WebAppResourceGroup"
  location                 = "South Central US"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Database Creation
resource "azurerm_sql_database" "WebAppDatabase" {
  name                = "WebAppDatabase"
  resource_group_name = "WebAppResourceGroup"
  location            = "South Central US"
  server_name         = "WebAppDatabaseServer"
  edition             = "Basic"
  requested_service_objective_name = "Basic"
  max_size_bytes      = "21474836480"
  tags = {
    Name = "WebAppDatabase"
  }
}

# Database Server Creation
resource "azurerm_sql_server" "WebAppDatabaseServer" {
  name                = "WebAppDatabaseServer"
  resource_group_name = "WebAppResourceGroup"
  location            = "South Central US"
  version             = "12.0"
  administrator_login = "adminuser"
  administrator_login_password = "P@ssw0rd1234!"
  tags = {
    Name = "WebAppDatabaseServer"
  }
}

# Database Firewall Rule Creation
resource "azurerm_sql_firewall_rule" "WebAppDatabaseServer_firewall_rule" {
  name                = "WebAppDatabaseServer_firewall_rule"
  resource_group_name = "WebAppResourceGroup"
  server_name         = azurerm_sql_server.WebAppDatabaseServer.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}