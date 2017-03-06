import src.config as config


class Thermometer:

    def __init__(self, thermometer_id):
        self.thermometer_id = thermometer_id

    def current_temperature(self):

        path_to_data_file = '%s%s%s' % (config.PATH_PREFIX, self.thermometer_id, config.PATH_SUFFIX)

        data_file = open(path_to_data_file)
        data = data_file.read()
        data_file.close()

        temperature = float(data.split("\n")[1].split(" ")[9][2:]) / 1000

        return temperature
