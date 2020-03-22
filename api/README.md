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

## Methods


### List Locations

`GET` /api/locations

Optional Params:
* `q` string - Freeform search query

Optional Params:
* `per_page` int
* `page_num` int

### Create Report

`POST` /api/reports

Optional Params:
* `community_id` string
* `infected` int
* `cured` int
* `dead` int
* `report_date` date (YYYY-MM-DD)
* `origin` string

### List Reports

`GET` /api/reports

Optional Params:
* `per_page` int
* `page_num` int


### Get one Report

`GET` /api/reports/{id}


### List Community Reports

`GET` /api/communities/{community_id}/reports


Optional Params:
* `per_page` int
* `page_num` int