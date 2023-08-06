import logging


class FunctionCallNode:
    def __init__(self, box, generator):
        self.box = box
        self.generator = generator
        self._result_prefix = "fn"
        logging.debug("Constructed function call node")

    def to_python(
        self, indent="    ", store_result_in_variable=True, called_by_next_box=False
    ):
        logging.debug("Generating Python for function call node")
        result = indent

        function_name = self.box.box_header
        function_name = function_name[2 : len(function_name) - 1]

        function_args = []

        for port in self.box.input_data_flow_ports:
            input_port = self.generator._find_destination_connection(port, "left")
            input_box = self.generator.port_box_map[input_port]
            function_args.append(
                self.generator._get_output_data_name(input_box, input_port)
            )

        logging.debug(
            "  Found " + str(len(function_args)) + " arguments to function call"
        )

        # Check if function result is used
        if store_result_in_variable and len(self.box.output_data_flow_ports) > 0:
            logging.debug(
                "  Function result will be used. Creating a variable to store the result"
            )
            fn_result = self._result_prefix + "_" + self.box.uuid_short() + "_result"
            self.generator.temp_results[self.box] = fn_result
            result += fn_result + " = "
            logging.debug("  Result variable name: " + fn_result)

        result += function_name
        result += "("
        for i, arg in enumerate(function_args):
            result += arg
            if i < len(function_args) - 1:
                result += ", "

        result += ")\n"
        return result
