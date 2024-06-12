

# Provider Configuration
provider "azurerm" {
  features {}
  subscription_id = "SUBSCRIPTION_ID"
  client_id       = "CLIENT_ID"
  client_secret   = "CLIENT_SECRET"
  tenant_id       = "TENANT_ID"
}

# VPC Creation
resource "azurerm_virtual_network" "myvnet" {
  name                = "myvnet"
  address_space       = ["195.36.153.1/24"]
  location            = "East US"
  resource_group_name = "myresourcegroup"
}

# Subnet Creation
resource "azurerm_subnet" "mysubnet" {
  name                 = "mysubnet"
  resource_group_name  = "myresourcegroup"
  virtual_network_name = azurerm_virtual_network.myvnet.name
  address_prefixes     = ["195.36.153.1/28"]
  location             = "East US"
}

# Internet Gateway Creation
resource "azurerm_virtual_network_gateway" "myvnet_igw" {
  name                = "myvnet_igw"
  location            = "East US"
  resource_group_name = "myresourcegroup"
  type                = "IPsec"
  vpn_type            = "RouteBased"
  sku                 = "VpnGw1"
  vnet_id             = azurerm_virtual_network.myvnet.id
}

# Route Table Creation
resource "azurerm_route_table" "myvnet_route_table" {
  name                = "myvnet_route_table"
  location            = "East US"
  resource_group_name = "myresourcegroup"
  disable_bgp_route_propagation = false
  virtual_network_name = azurerm_virtual_network.myvnet.name
  route {
    name                   = "route1"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualNetworkGateway"
    next_hop_in_ip_address = azurerm_virtual_network_gateway.myvnet_igw.gateway_ip_configuration[0].private_ip_address
  }
}

# Route Table Association
resource "azurerm_subnet_route_table_association" "myvnet_route_table_association" {
  subnet_id      = azurerm_subnet.mysubnet.id
  route_table_id = azurerm_route_table.myvnet_route_table.id
}

# Security Group Creation
resource "azurerm_network_security_group" "alpha" {
  name                = "alpha"
  location            = "East US"
  resource_group_name = "myresourcegroup"
  security_rule {
    name                       = "allow_ssh"
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
    name                       = "allow_all"
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
resource "azurerm_virtual_machine" "aaa" {
  name                  = "aaa"
  location              = "East US"
  resource_group_name   = "myresourcegroup"
  network_interface_ids = [azurerm_network_interface.aaa.id]
  vm_size               = "Standard_A1"
  delete_os_disk_on_termination = true
  delete_data_disks_on_termination = true
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
  os_profile {
    computer_name  = "aaa"
    admin_username = "adminuser"
    admin_password = "P@ssw0rd1234!"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
  tags = {
    Name = "aaa"
  }
}

# Storage Account Creation
resource "azurerm_storage_account" "myacc" {
  name                     = "myacc"
  resource_group_name      = "myresourcegroup"
  location                 = "East US"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Database Creation
resource "azurerm_cosmosdb_account" "mydb" {
  name                = "mydb"
  location            = "East US"
  resource_group_name = "myresourcegroup"
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy {
    consistency_level = "Session"
  }
  capabilities {
    name = "EnableAutoScale"
  }
  database {
    name = "mydb"
    throughput = 400
  }
}