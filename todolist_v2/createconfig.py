import configparser


def create_config():
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config['Database'] = {'dbname': 'your_dbname',
                          'user': 'your_user',
                          'password': 'your_password',
                          'host': 'your_host',}

    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    create_config()