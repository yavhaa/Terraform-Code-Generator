

# Provider Configuration
provider "azurerm" {
  features {}
  subscription_id = "SUBSCRIPTION_ID"
  client_id       = "CLIENT_ID"
  client_secret   = "CLIENT_SECRET"
  tenant_id       = "TENANT_ID"
}

# VPC Creation
resource "azurerm_virtual_network" "WebAppVNet" {
  name                = "WebAppVNet"
  address_space       = ["16.0.0.0/16"]
  location            = "East US 2"
  resource_group_name = "WebAppResourceGroup"
}

# Subnet Creation
resource "azurerm_subnet" "WebAppSubnet" {
  name                 = "WebAppSubnet"
  resource_group_name  = "WebAppResourceGroup"
  virtual_network_name = azurerm_virtual_network.WebAppVNet.name
  address_prefixes     = ["10.0.1.0/24"]
  location             = "East US 2"
}

# Internet Gateway Creation
resource "azurerm_public_ip" "WebAppVNet_igw_public_ip" {
  name                = "WebAppVNet_igw_public_ip"
  location            = "East US 2"
  resource_group_name = "WebAppResourceGroup"
  allocation_method   = "Dynamic"
}

resource "azurerm_subnet_network_security_group_association" "WebAppSubnet_nsg_association" {
  subnet_id                 = azurerm_subnet.WebAppSubnet.id
  network_security_group_id = azurerm_network_security_group.WebAppSecurityGroup.id
}

# Route Table Creation
resource "azurerm_route_table" "WebAppVNet_route_table" {
  name                = "WebAppVNet_route_table"
  location            = "East US 2"
  resource_group_name = "WebAppResourceGroup"
}

resource "azurerm_route" "WebAppVNet_route" {
  name                   = "WebAppVNet_route"
  resource_group_name    = "WebAppResourceGroup"
  route_table_name       = azurerm_route_table.WebAppVNet_route_table.name
  address_prefix         = "0.0.0.0/0"
  next_hop_type          = "VirtualAppliance"
  next_hop_in_ip_address = azurerm_public_ip.WebAppVNet_igw_public_ip.ip_address
}

# Route Table Association
resource "azurerm_subnet_route_table_association" "WebAppSubnet_route_table_association" {
  subnet_id      = azurerm_subnet.WebAppSubnet.id
  route_table_id = azurerm_route_table.WebAppVNet_route_table.id
}

# Security Group Creation
resource "azurerm_network_security_group" "WebAppSecurityGroup" {
  name                = "WebAppSecurityGroup"
  location            = "East US 2"
  resource_group_name = "WebAppResourceGroup"

  security_rule {
    name                       = "SSH"
    priority                   = 1001
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
    priority                   = 1002
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
resource "azurerm_linux_virtual_machine" "WebAppDeployment" {
  name                = "WebAppDeployment"
  location            = "East US 2"
  resource_group_name = "WebAppResourceGroup"
  network_interface_ids = [
    azurerm_network_interface.WebAppDeployment_nic.id
  ]
  size                = "Standard_A2_v2"
  admin_username      = "adminuser"
  admin_password      = "P@ssw0rd1234!"
  computer_name       = "WebAppDeployment"
  os_disk {
    name              = "WebAppDeployment_osdisk"
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  tags = {
    Name = "WebAppDeployment"
  }
}

# Storage Account Creation
resource "azurerm_storage_account" "webappstorageaccount" {
  name                     = "webappstorageaccount"
  resource_group_name      = "WebAppResourceGroup"
  location                 = "East US 2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Database Creation
resource "azurerm_mssql_database" "Mydatabase" {
  name                = "Mydatabase"
  resource_group_name = "WebAppResourceGroup"
  location            = "East US 2"
  server_name         = "Mydatabase"
  edition             = "Basic"
  requested_service_objective_name = "Basic"
  collation_name      = "SQL_Latin1_General_CP1_CI_AS"
  max_size_bytes      = "21474836480"
  tags = {
    Name = "Mydatabase"
  }
}

# Database Server Creation
resource "azurerm_mssql_server" "Mydatabase" {
  name                = "Mydatabase"
  resource_group_name = "WebAppResourceGroup"
  location            = "East US 2"
  version             = "12.0"
  administrator_login = "adminuser"
  administrator_login_password = "P@ssw0rd1234!"
  tags = {
    Name = "Mydatabase"
  }
}

# Database Firewall Rule Creation
resource "azurerm_mssql_firewall_rule" "Mydatabase" {
  name                = "Mydatabase"
  resource_group_name = "WebAppResourceGroup"
  server_name         = azurerm_mssql_server.Mydatabase.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}