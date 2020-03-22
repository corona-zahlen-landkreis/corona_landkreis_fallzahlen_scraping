# Installation

make sure you got the php-sqlite extension installed

```
// Install Vendors
$ composer install

// Database Migration
$ vendor/bin/phinx migrate

// Run development
$ cd public;
$ php -S localhost:8080
```

## Calls:

### Create Report
```
Method Post:

http://localhost:8080/api/reports
?community_id=321
&infected=5
&cured=5
&dead=0
&report_date=2020-03-21,
&origin=webscraper
```

// List Reports

```
Method Get

http://localhost:8080/api/reports


http://localhost:8080/api/reports/{id}

```

// List Reports for a Community
```
Method Get
http://localhost:8080/api/communities/{community_id}/reports

```