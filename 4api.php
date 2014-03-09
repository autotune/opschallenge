<?php
require 'vendor/autoload.php';

echo "What is the container name: ";
$temp2 = fopen ("php://stdin","r");
$contName = fgets($temp2);

use OpenCloud\Rackspace;
use OpenCloud\ObjectStore\Resource\DataObject;
$client = new Rackspace(Rackspace::US_IDENTITY_ENDPOINT, array(
    'username' => '',
    'apiKey'   => ''
));


// create service object use object store in 'ORD'
$service = $client->objectStoreService('cloudFiles', 'ORD');
$containerList = $service->listContainers();
// define which file to open, and be ready to scale file list
/** $files = array(
	array(
	     'name'  => 'test.html', 
	     '/var/www/html/test.html', 'r+'
	)
); **/

$data = fopen('/var/www/html/test.html', 'r+');

// return list of containers

while ($container = $containerList->next()) {
	// store list of container objects in array
	$containers[] = $container->name; 
	}; 

	// check if container exists and exit if it does

	// foreach ($containers as $contName) {
	//	printf("Container name: %s\n", $contName);

// check if container is equal to list. If not, ask for new name
foreach ($containers as $container) {
	if ($container == $contName) {
		$contExist = "$contName";
		printf("Container $contExist exists, try again\n");
		die;
	}
}


try {
	$response = $service->createContainer("$contName");
    	print "Container name: $contName";
	// upload file, enable streaming, and get streaming URI
	// getContainer is the first property we need!
	$container = $service->getContainer($contName);
	$container->uploadObject('test.html', $data);
	$container->enableCdn();
	$cdn = $container->getCdn();
	$uri = $cdn->getCdnStreamingUri();
	printf("URL: $uri\n");
}


catch (\Guzzle\Http\Exception\BadResponseException $e) {

	$responseBody = (string) $e->getResponse() ->getBody();
	$statusCode   = $e->getResponse()->getStatusCode();
	$headers      = $e->getResponse()->getHeaderLines();
	
	echo sprintf("Status: %s\nBody: %s\nHeaders: %s", $statusCode, $responseBody, implode(', ', $headers));


}

?>
