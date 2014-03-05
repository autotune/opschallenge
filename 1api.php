<?php
require 'vendor/autoload.php';
require 'auth.php';

$service = $client->computeService('cloudServersOpenStack', 'ORD');
$compute = $client->computeService('cloudServersOpenStack', 'ORD');
$server = $compute->server();
$serverName->name = 'Test Server2';
$flavors=$compute->flavorList();
$images = $compute->imageList();

// flavor time
while ($flavor = $flavors->next()) {
	if (strpos($flavor->name, '1GB') !== false) {
		$oneGb = $flavor;
		break;
	}
}

// we want to use CentOS as the image
while ($image = $images->next()) {
   if (strpos($image->name, 'CentOS') !== false) {
	$centos = $image;
        break;
   }

}

// create server with image id. Check for errors
try {
    $response = $server->create(array(
	'name'	=> "Test Server3",
	'image' => $centos, 
        'flavor' => $oneGb,
	)
     );
}


catch (\Guzzle\Http\Exception\BadResponseException $e) {

	$responseBody = (string) $e->getResponse() ->getBody();
	$statusCode   = $e->getResponse()->getStatusCode();
	$headers      = $e->getResponse()->getHeaderLines();
    	
	echo sprintf("Status: %s\nBody: %s\nHeaders: %s", $statusCode, $responseBody, implode(', ', $headers));


}

// we must wait for it to complete before the IP is set
use OpenCloud\Compute\Constants\ServerState;

$callback = function($server) {
    if (!empty($server->error)) {
        var_dump($server->error);
        exit;
    } else {
        echo sprintf(
            "Waiting on %s/%-12s %4s%%\n",
            $server->name(),
            $server->status(),
            isset($server->progress) ? $server->progress : 0
        );
    }
};

$server->waitFor(ServerState::ACTIVE, 600, $callback);
$serverID=$server->id;
$addr = $compute->server("$serverID");
echo "<html>\n";
echo "<body>\n"; 
echo "<br>\n";
echo "\n**********************\n";
echo "<br>\n";
echo "AdminPass: $server->adminPass\n<br>\n";
echo "IP Address: $addr->accessIPv4\n<br>\n";
echo "\n**********************\n\n";
echo '</html>';
echo '</body>';

?>
