<?php
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

$app->get('/reports[/{id:.*}]', function (Request $request, Response $response, array $args) {
    try {
        if (is_numeric($args['id'])) {
            $report = ORM::for_table('reports')->find_one($args['id']);
            $jsonData = $report ? $report->as_array() : null;
        } else {
            $reports = ORM::for_table('reports')->find_many();
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

$app->post('/reports', function (Request $request, Response $response, array $args) {
    try {
        $report = ORM::for_table('reports')->create();

        $report->community_id = $request->getParam('community_id');
        $report->infected = $request->getParam('infected');
        $report->cured = $request->getParam('cured');
        $report->dead = $request->getParam('dead');
        $report->report_date = $request->getParam('report_date');

        $report->save();
        $response->getBody()->write(json_encode($report->as_array()));
    } catch (\Throwable $t) {
        $response->setSgetBody()->write($t->getMessage());
    }

    return $response;
});

$app->run();