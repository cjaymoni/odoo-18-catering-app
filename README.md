# 🍽️ Catering Management System - Odoo 18

A comprehensive catering management solution built on Odoo 18 with Docker deployment, featuring multi-user access, booking management, menu administration, and WhatsApp integration.

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Quick Start](#-quick-start)
- [User Accounts & Permissions](#-user-accounts--permissions)
- [Database Access](#-database-access)
- [Security Configuration](#-security-configuration)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)

## 🚀 Features

### Core Functionality

- **Event Booking Management** - Complete booking lifecycle with status tracking
- **Menu & Service Administration** - Dynamic menu categories and service offerings
- **Multi-User Access Control** - Role-based permissions (Manager/Staff/Client)
- **Customer Feedback System** - Rating and review collection
- **WhatsApp Integration** - Automated messaging and notifications
- **Sales Order Integration** - Automatic order generation from bookings
- **Mobile-Responsive UI** - Touch-friendly interface for all devices

### Business Capabilities

- **Client Self-Service** - Customers can create and manage their own bookings
- **Staff Operations** - Booking management and customer interaction tools
- **Manager Dashboard** - Complete system oversight and configuration
- **Reporting & Analytics** - Built-in Odoo reporting capabilities
- **Document Generation** - Automated invoices and booking confirmations

## 🏗️ System Architecture

### Technology Stack

- **Backend**: Odoo 18.0 (Python/PostgreSQL)
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (via Odoo)
- **Admin Interface**: PgAdmin 4

### Container Services

- **odoo-catering**: Main Odoo application (Port 8069)
- **odoo-postgres**: PostgreSQL database (Port 5432)
- **odoo-pgadmin**: Database administration (Port 8080)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- 4GB+ RAM recommended
- Ports 8069, 5432, 8080 available

### Installation

1. **Clone or Download** the project files

```bash
cd catering-odoo
```

2. **Start the System**

```bash
docker-compose up -d
```

3. **Wait for Initialization** (first startup takes 2-3 minutes)

```bash
# Check if ready
curl -s http://localhost:8069/web/database/selector
```

4. **Create Database & Install Module** (if not already done)

```bash
# Replace <DB_NAME> with your actual Odoo database (e.g., catering-db)
docker-compose exec web odoo -d <DB_NAME> -i cater --stop-after-init --without-demo=False
docker-compose restart web
```

### Access URLs

- **Main Application**: http://localhost:8069
- **Database Admin**: http://localhost:8080
- **Database**: Create from the web UI or use your existing DB (e.g., `catering-db`)

## 👥 User Accounts & Permissions

### Default User Accounts

| **Role**    | **Username**            | **Password** | **Access Level**     |
| ----------- | ----------------------- | ------------ | -------------------- |
| **Admin**   | `admin`                 | `admin`      | System Administrator |
| **Manager** | `manager@catering.test` | `manager123` | Full Business Access |
| **Staff**   | `staff@catering.test`   | `staff123`   | Operational Access   |
| **Client**  | `client@catering.test`  | `client123`  | Self-Service Portal  |

### Permission Matrix

#### 👑 **MANAGER** (Full Control)

- ✅ **Menu Management**: Create/edit/delete categories and items
- ✅ **Service Configuration**: Manage all service offerings
- ✅ **Booking Administration**: Full booking lifecycle management
- ✅ **System Configuration**: WhatsApp, reporting, user management
- ✅ **Financial Operations**: Pricing, invoicing, sales orders
- ✅ **Data Management**: Delete records, audit trails

#### 👤 **STAFF** (Operational Access)

- ✅ **Booking Management**: Create/edit bookings (cannot delete)
- ✅ **Menu Updates**: Modify menu items and categories
- ✅ **Customer Service**: Handle feedback and communications
- ✅ **Order Processing**: Manage booking lines and services
- ❌ **System Config**: Limited access to configuration
- ❌ **Financial**: Cannot modify pricing or delete records

#### 🧑‍💼 **CLIENT** (Self-Service)

- ✅ **Own Bookings**: Create/edit personal bookings only
- ✅ **Menu Browsing**: View all available menu items
- ✅ **Feedback**: Submit reviews for completed services
- ✅ **Service Selection**: Add services to bookings
- ❌ **Other Clients**: Cannot see other customers' data
- ❌ **Administration**: No access to system settings

### Security Features

- **Data Isolation**: Clients only see their own bookings
- **Domain Filtering**: `[('partner_id.user_ids', 'in', [user.id])]`
- **Hierarchical Permissions**: Manager > Staff > Client
- **Audit Trails**: All changes tracked with user attribution

## 🗄️ Database Access

### Master Credentials

- **Database Name**: `<DB_NAME>` (example: `catering-db`)
- **Username**: `odoo`
- **Password**: `odoo_password`
- **Host**: `localhost`
- **Port**: `5432`

### PgAdmin Access

- **URL**: http://localhost:8080
- **Email**: `pgadmin@mail.com`
- **Password**: `pgadmin`

### Connection Strings

```bash
# PostgreSQL Direct
psql postgresql://odoo:odoo_password@localhost:5432/<DB_NAME>

# Docker Internal
docker-compose exec db psql -U odoo -d <DB_NAME>
```

## 🔒 Security Configuration

### Group Structure

```xml
<!-- Hierarchy: Manager > Staff > Client -->
<record id="catering_manager_group" model="res.groups">
    <field name="implied_ids" eval="[(4, ref('catering_staff_group'))]"/>
</record>
<record id="catering_staff_group" model="res.groups">
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
<record id="catering_client_group" model="res.groups">
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
```

### Record Rules Examples

```xml
<!-- Clients only see own bookings -->
<field name="domain_force">[('partner_id.user_ids', 'in', [user.id])]</field>

<!-- Staff can access all operational data -->
<field name="groups" eval="[(4, ref('catering_staff_group'))]"/>
```

### Models & Access Control

| **Model**                | **Manager** | **Staff** | **Client** |
| ------------------------ | ----------- | --------- | ---------- |
| `cater.event.booking`    | CRUD        | RWC       | RWC (own)  |
| `cater.menu.item`        | CRUD        | RWC       | R          |
| `cater.feedback`         | CRUD        | RW        | RWC (own)  |
| `cater.whatsapp.service` | CRUD        | R         | -          |
| `sale.order`             | CRUD        | RWC       | RWC (own)  |
| `sale.order.line`        | CRUD        | RWC       | RWC (own)  |
| `product.product`        | CRUD        | RWC       | C          |
| `product.template`       | CRUD        | RWC       | C          |

**Legend:** R=Read, W=Write, C=Create, D=Delete, "own"=domain filtered to user's own records

## 🔧 Troubleshooting

### Common Issues

#### Database Creation Error

```bash
# Clean restart with fresh volumes
docker-compose down -v
docker-compose up -d
# Wait for postgres to initialize, then create database
```

#### Permission Errors

```bash
# Update module after permission changes
docker-compose exec web odoo -u cater -d <DB_NAME> --stop-after-init
docker-compose restart web
```

#### Client Booking Issues

- **Sales Order Error**: Ensure client has sales permissions
- **Product Creation Error**: Verify product access permissions
- **Staff Product Error**: Staff users need product create permissions for booking workflow
- **Domain Filter Issues**: Check partner-user relationships

#### Module Updates

```bash
# Update module with new changes
docker-compose exec web odoo -u cater -d <DB_NAME> --stop-after-init
docker-compose restart web
```

### Log Access

```bash
# View container logs
docker-compose logs web
docker-compose logs db

# Follow live logs
docker-compose logs -f web
```

### Database Reset

```bash
# Complete reset (CAUTION: Deletes all data)
docker-compose down -v
docker-compose up -d
# Recreate database and reinstall module
docker-compose exec web odoo -d <DB_NAME> -i cater --stop-after-init --without-demo=False
```

## 🛠️ Development

### Project Structure

```
catering-odoo/
├── addons/cater/           # Main module
│   ├── models/             # Business logic
│   ├── views/              # UI definitions
│   ├── security/           # Access control
│   ├── data/               # Demo data
│   └── static/             # CSS/JS assets
├── config/                 # Odoo configuration
├── docker-compose.yml      # Container orchestration
└── README.md              # This file
```

### Key Files

- **`addons/cater/__manifest__.py`**: Module definition
- **`addons/cater/models/event_booking.py`**: Core booking logic
- **`addons/cater/security/ir.model.access.csv`**: Permission matrix
- **`addons/cater/security/security.xml`**: Groups and record rules
- **`addons/cater/views/portal_views.xml`**: Client interface

### Adding Features

1. **Create Model**: Add to `models/` directory
2. **Add Permissions**: Update `security/` files
3. **Create Views**: Add XML views to `views/`
4. **Update Module**: Run update command
5. **Test**: Validate with different user types

### Testing

```bash
# Run security validation
./ui_security_test.sh

# Test with different users
# Login as each user type and validate permissions
```

### Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Access Odoo shell
docker-compose exec web odoo shell -d <DB_NAME>

# Restart Odoo (after code changes)
docker-compose restart web

# Update module
docker-compose exec web odoo -u cater -d <DB_NAME> --stop-after-init

# Backup database
docker-compose exec db pg_dump -U odoo <DB_NAME> > backup.sql
```

## 📞 Support

### System Information

- **Odoo Version**: 18.0-20250710
- **PostgreSQL**: 15
- **Python**: 3.x (via Odoo container)
- **Architecture**: Docker containerized

### Important Notes

- First startup takes 2-3 minutes for database initialization
- Demo data includes sample bookings and menu items
- All passwords are development defaults - change for production
- Mobile interface optimized for touch devices
- WhatsApp integration requires API configuration

### Production Deployment

- Change all default passwords
- Configure SSL/HTTPS
- Set up proper backup procedures
- Configure WhatsApp API credentials
- Set up email server for notifications

## 📧 Email Configuration

### Google SMTP Setup

To enable email notifications for booking confirmations, you need to configure Google SMTP:

#### 1. **Enable 2-Factor Authentication** on your Gmail account

- Go to [Google Account Settings](https://myaccount.google.com)
- Security → 2-Step Verification → Turn on

#### 2. **Generate App Password**

- Google Account → Security → 2-Step Verification
- Scroll down to "App passwords"
- Select app: "Mail"
- Select device: "Other (custom name)" → Enter "Odoo Catering"
- Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

#### 3. **Update Configuration**

Edit `config/odoo.conf` and replace:

```properties
email_from = your-actual-email@gmail.com
smtp_user = your-actual-email@gmail.com
smtp_password = your-16-char-app-password
```

#### 4. **Restart Services**

```bash
docker-compose restart web
```

#### 5. **Test Email Configuration**

- Login as staff user
- Create and confirm a booking
- Email notifications will be sent to customers

### Email Features

- **Booking Confirmations**: Automatic emails when bookings are confirmed
- **Status Updates**: Notifications for booking state changes
- **Activity Tracking**: Internal notifications in booking chatter
- **Customer Communications**: Professional email templates

---

**🍽️ Happy Catering Management!**

_For technical support or feature requests, please refer to the module documentation or contact your system administrator._

## 💬 WhatsApp (Twilio) Setup

1. Configure credentials in Odoo

- Go to Catering → WhatsApp → Configuration
- Set Account SID and Auth Token
- Sandbox: set From Number to +14155238886 and ensure recipients have joined your sandbox phrase
- Production: Prefer Messaging Service SID (recommended). If set, From is ignored.
- Click "Test Connection" to verify credentials

2. Expose Odoo and set base URL

- Run a public HTTPS tunnel (e.g., ngrok): `ngrok http 8069`
- Copy the HTTPS URL and set in Odoo: Settings → Technical → System Parameters → `web.base.url`
- Note: The app automatically includes a StatusCallback only when `web.base.url` is a public http(s) URL (not localhost)

3. Twilio Sandbox/Webhook settings

- When a message comes in: `https://<your-public-host>/whatsapp/webhook` (Method: POST)
- Status callback URL: `https://<your-public-host>/whatsapp/webhook` (Method: POST)
- Save. You can use the same endpoint for both inbound and status callbacks.

4. Outbound and delivery tracking

- Booking confirmation sends on Confirm; feedback send on Complete
- Logs at Catering → WhatsApp → Logs now include the Twilio SID and statuses (queued/sent/delivered/read)
- Inbound WhatsApp messages are logged with status `received`

5. Templates (optional)

- The service supports Twilio Content Templates via `send_template(to_number, content_sid, variables)`
- Example variables: `{ "1": "12/1", "2": "3pm" }`

6. Container image

- The custom image installs `twilio` in the Odoo container (no Flask required)
- Rebuild after changes: `docker-compose build --no-cache web && docker-compose up -d`
