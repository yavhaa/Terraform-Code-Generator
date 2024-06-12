Below is the Terraform script for the specified Azure cloud infrastructure configuration, followed by a rough cost estimation for one year:

### Terraform Script

```hcl
provider "azurerm" {
  features {}
  region = "West US 3"
}

resource "azurerm_virtual_network" "WebAppVnet" {
  name                = "WebAppVnet"
  address_space       = ["16.0.0.0/16"]
  location            = "West US 3"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "mysubnet" {
  name                 = "mysubnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.WebAppVnet.name
  address_prefixes     = ["16.0.1.0/24"]
}

resource "azurerm_network_security_group" "Alpha" {
  name                = "Alpha"
  location            = "West US 3"
  resource_group_name = azurerm_resource_group.main.name

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
    name                       = "AllOutbound"
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

resource "azurerm_network_interface" "main" {
  name                = "WebAppDeploymentNIC"
  location            = "West US 3"
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.mysubnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "WebAppDeployment" {
  name                = "WebAppDeployment"
  resource_group_name = azurerm_resource_group.main.name
  location            = "West US 3"
  size                = "Standard_A2_v2"
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  os_disk {
    caching              = "ReadWrite"
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

resource "azurerm_storage_account" "myacc" {
  name                     = "myacc"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = "West US 3"
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_sql_database" "WebAppDatabase" {
  name                = "WebAppDatabase"
  resource_group_name = azurerm_resource_group.main.name
  location            = "West US 3"
  server_name         = azurerm_sql_server.main.name
  max_size_gb         = 20
}

resource "azurerm_sql_server" "main" {
  name                         = "WebAppSQLServer"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = "West US 3"
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = "Password123!"
}
```

### Cost Estimation

1. **Azure Virtual Machine (Standard A2 v2)**: Approximately $70/month
2. **Azure SQL Database**: Basic tier with 20 GB storage is around $5/month.
3. **Storage Account (Standard LRS)**: Minimal cost, typically less than $2/month for moderate usage.
4. **Network and other resources**: Generally minimal cost, but dependent on traffic and rules.

**Total Estimated Cost for 1 Year**: 
- VM: $70 * 12 = $840
- SQL Database: $5 * 12 = $60
- Storage Account: $2 * 12 = $24
- Additional Costs: ~$50 (estimated)

**Grand Total**: ~$974/year

This is a rough estimate and actual costs may vary based on actual usage, specific Azure pricing adjustments, and additional services or resources used.