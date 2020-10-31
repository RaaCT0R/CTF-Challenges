console.log("Script loaded successfully ");
Java.perform(function x() { //Silently fails without the sleep from the python code
	console.log("Inside java perform function");
	//get a wrapper for our class
	var my_class1 = Java.use("com.example.razictf_2.switcher"); // freind page
	//replace the original implmenetation of the function `fun` with our custom function
	my_class1.run.implementation = function (i) {
		//print the original arguments
		console.log(": run(" + i + ")");
		//call the original implementation of `fun` with args (2,5)
		i = 0;
		var ret_value = this.run(i);
		return ret_value;
	}
});
