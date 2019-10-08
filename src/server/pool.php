<?php

if ($_GET['type'] == 'json') {
    $json = file_get_contents("data.json");
    header("Content-type:application/json;charset=utf-8");
    echo $json;
} else {
    http_response_code(400);
    echo "400: bad request";
}
