<?php
set_time_limit(0); // タイムアウトさせない
$port = 19455; // ポート指定

class MySocket
{
    private  $socket;
    private  $client;

    public function __construct()
    {

    }

    public function __destruct()
    {
        if (is_resource($this->client)) {
            socket_close($this->client);
        }

        if (is_resource($this->socket)) {
            socket_close($this->socket);
        }
    }

    public function listen()
    {
        $port = 19455;
        $this->socket = socket_create_listen($port);
        if ($this->socket === false) {
            throw new RuntimeException();
        }

        $this->client = socket_accept($this->socket);
        if ($this->client === false) {
            throw new RuntimeException();
        }

        $request = socket_read($this->client, 4096, PHP_BINARY_READ);
        list($header, $body) = explode("\r\n\r\n", $request);

        $response = json_decode($body, true);

        if ($response['RequestType'] == 'associate') {
            $result = $response;
            $result['Id'] = 'wakaran';
            $result['Success'] = true;
            $http_response = $this->createHttpResponse(json_encode($result));
            socket_write($this->client, $http_response);
        } else if ($response['RequestType'] == 'get-logins') {
            var_dump($response);
        }
    }

    private function createHttpResponse($body)
    {
        $data = array();
        $data[] = 'HTTP/1.1 200 OK';
        $data[] = 'Connection: close';
        $data[] = 'Content-Type: application/json; charset=utf-8';
        $data[] = '';
        $data[] = $body;
        $data[] = '';

        $header = implode("\r\n", $data);

        return $header;
    }

}

$socket = new MySocket();
$socket->listen();

function request_verify($response)
{
    $success = false;
    $crypted = base64_decode($response['Verifier']);
}
