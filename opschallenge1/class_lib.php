<?php
	class person { // set class aka blueprint/template
		var $name; // set property
			public $song_list;
			protected $practice_room;
			public $practice_time;

			function __construct($persons_name) { // call construct with persons_name arguement
				$this->name = $persons_name;
			}

			function set_name($new_name) { // set method 
				$this->name = $new_name; // this variable is the name of the function-defined arguement
			}

			function get_name() {
				return $this->name;
			}

	}

	class drums {
		var $practice;
		
                       function set_practice_time($practice_time){
                       		$this->practice_time = $practice_time;
                        }

                        function get_practice_time() {
                                return $this->practice_time;
                        }

	}
?>
