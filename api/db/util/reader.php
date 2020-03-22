<?php

class Reader extends \ORM {

    public static function checkPagination(\ORM $model, \Psr\Http\Message\ServerRequestInterface $request): void
    {
        $pageNum = intval($request->getParam('page_num')) - 1;
        $perPage = intval($request->getParam('per_page'));
        if ($pageNum < 0) {
            $pageNum = 0;
        }

        if ($perPage < 0) {
            $perPage = 20;
        }

        if ($perPage > 100) {
            $perPage = 100;
        }

        $model->limit($perPage);
        $model->offset($perPage * $pageNum);
    }
}