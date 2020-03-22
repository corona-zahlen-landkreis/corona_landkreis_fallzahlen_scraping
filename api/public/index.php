<?php
error_reporting(E_ALL);

// Deliver Static Files specially for Php CLI Server
if (PHP_SAPI == 'cli-server') {
    $url  = parse_url($_SERVER['REQUEST_URI']);
    $file = __DIR__ . $url['path'];

    // check the file types, only serve standard files
    if (preg_match('/\.(?:png|js|jpg|jpeg|gif|vue|css)$/', $file)) {
        // does the file exist? If so, return it
        if (is_file($file))
            return false;

        // file does not exist. return a 404
        header($_SERVER['SERVER_PROTOCOL'].' 404 Not Found');
        printf('"%s" does not exist', $_SERVER['REQUEST_URI']);
        return false;
    }
}

use \Psr\Http\Message\ServerRequestInterface as Request;
use \Psr\Http\Message\ResponseInterface as Response;

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/../bootstrap/database.php';
require_once __DIR__ . '/../db/idiorm.php';

$app = new \Slim\App([
    'settings' => [
        'displayErrorDetails' => true
    ]
]);

// TODO: Move this into ../bootstrap/routes
// TODO: create controllers

// Enable CORS
$app->add(function ($req, $res, $next) {
    $response = $next($req, $res);
    return $response
            ->withHeader('Access-Control-Allow-Origin', '*')
            ->withHeader('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, Origin, Authorization')
            ->withHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS');
});

$app->get('/api/locations', function (Request $request, Response $response, array $args) {
    try {
        $query = $request->getParam('q');
        $model = ORM::for_table('locations');

        if ($query !== null) {
            $model->where_raw('(community_id LIKE ? OR community LIKE ?)', [$query.'%', '%'.$query.'%']);
        }

        $model->limit(20);
        $locations = $model->find_many();
        $jsonData = [];

        foreach($locations as $location) {
            $jsonData[] = $location->as_array();
        }

        $response->getBody()->write(json_encode($jsonData));
    } catch (\Throwable $t) {
        $response->getBody()->write($t->getMessage());
    }

    return $response;
});

$app->get('/api/reports[/{id:.*}]', function (Request $request, Response $response, array $args) {
    try {
        $model = ORM::for_table('reports')->table_alias('rp');
        $model->join('locations', ['rp.community_id', '=', 'loc.community_id'], 'loc');

        if (isset($args['id']) && is_numeric($args['id'])) {
            $report = $model->find_one($args['id']);
            $jsonData = $report ? $report->as_array() : null;
        } else {
            $model->limit(50);
            $reports = $model->find_many();
            $jsonData = [];

            foreach($reports as $report) {
                $jsonData[] = $report->as_array();
            }
        }

        $response->getBody()->write(json_encode($jsonData));
    } catch (\Throwable $t) {
        $response->getBody()->write($t->getMessage());
    }

    return $response;
});

$app->post('/api/reports', function (Request $request, Response $response, array $args) {
    try {
        $report = ORM::for_table('reports')->create();

        $report->community_id = $request->getParam('community_id');
        $report->infected = $request->getParam('infected');
        $report->cured = $request->getParam('cured');
        $report->dead = $request->getParam('dead');
        $report->report_date = $request->getParam('report_date');
        $report->origin = $request->getParam('origin');

        $report->save();
        $response->getBody()->write(json_encode($report->as_array()));
    } catch (\Throwable $t) {
        $response->setSgetBody()->write($t->getMessage());
    }

    return $response;
});

$app->get('/api/communities/{community_id}/reports', function (Request $request, Response $response, array $args) {
    try {
        $model = ORM::for_table('reports')->table_alias('rp');
        $model->join('locations', ['rp.community_id', '=', 'loc.community_id'], 'loc');

        $model->where_equal('rp.community_id', $args['community_id']);
        $model->limit(50);

        $reports = $model->find_many();
        $jsonData = [];
        foreach($reports as $report) {
            $jsonData[] = $report->as_array();
        }

        $response->getBody()->write(json_encode($jsonData));
    } catch (\Throwable $t) {
        $response->getBody()->write($t->getMessage());
    }

    return $response;
});

// Deliver UI
$app->any('/[{path:.*}]', function (Request $request, Response $response, array $args) {
    $response->getBody()->write(file_get_contents( __DIR__ . '/ui/index.html'));
    return $response;
});

$app->run();