

# Provider Configuration
provider "azurerm" {
  subscription_id = "SUBSCRIPTION_ID"
  client_id       = "CLIENT_ID"
  client_secret   = "CLIENT_SECRET"
  tenant_id       = "TENANT_ID"
  features {}
}

# VPC Creation
resource "azurerm_virtual_network" "my_vpc" {
  name                = "my_vpc"
  address_space       = ["10.0.0.0/16"]
  location            = "australiaeast"
}

# Subnet Creation
resource "azurerm_subnet" "my_subnet" {
  name                 = "my_subnet"
  address_prefix       = "10.0.1.0/24"
  virtual_network_name = azurerm_virtual_network.my_vpc.name
  location             = "australiaeast"
}

# Internet Gateway Creation
resource "azurerm_virtual_network_gateway" "my_igw" {
  name                = "my_igw"
  location            = "australiaeast"
  resource_group_name = azurerm_virtual_network.my_vpc.resource_group_name
  type                = "ipsec"
}

# Route Table Creation
resource "azurerm_route_table" "my_route_table" {
  name                = "my_route_table"
  location            = "australiaeast"
  resource_group_name = azurerm_virtual_network.my_vpc.resource_group_name

  route {
    name                   = "default_route"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualNetworkGateway"
    next_hop_in_ip_address = azurerm_virtual_network_gateway.my_igw.gateway_ip_configuration[0].ip_configuration[0].private_ip_address
  }
}

# Route Table Association
resource "azurerm_subnet_route_table_association" "my_route_table_association" {
  subnet_id      = azurerm_subnet.my_subnet.id
  route_table_id = azurerm_route_table.my_route_table.id
}

# Security Group Creation
resource "azurerm_network_security_group" "my_security_group" {
  name                = "my_security_group"
  location            = "australiaeast"
  resource_group_name = azurerm_virtual_network.my_vpc.resource_group_name

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
    name                       = "allow_all_outbound"
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
resource "azurerm_virtual_machine" "my_instance" {
  name                  = "my_instance"
  location              = "australiaeast"
  resource_group_name   = azurerm_virtual_network.my_vpc.resource_group_name
  network_interface_ids = [azurerm_network_interface.my_nic.id]
  vm_size               = "Standard_E-Series"
  tags = {
    Name = "my_template"
  }
}

# Storage Account Creation
resource "azurerm_storage_account" "my_storage_account" {
  name                     = "my_storage_account"
  resource_group_name      = azurerm_virtual_network.my_vpc.resource_group_name
  location                 = "australiaeast"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Database Creation
resource "azurerm_cosmosdb_account" "my_database" {
  name                = "my_database"
  location            = "australiaeast"
  resource_group_name = azurerm_virtual_network.my_vpc.resource_group_name
  offer_type          = "Standard"
  consistency_policy {
    consistency_level = "Session"
  }
  database {
    name = "my_database"
  }
}