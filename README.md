# IOT Manager
The project consists of a web application to manage a series of IoT devices. In addition to this application, several controllers have been implemented to test its operation.

The project is only a simulation of such devices, which are threads created to carry out a specific task.

## Installation
For the entire system to work correctly, it is necessary to install the virtual environment with the provided `requirements.txt`:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt
```

Once done, it is necessary to perform Django migrations, so that the database has the correct structure. Therefore, being in the `iot-manager` folder:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

With this, all requirements are met. The different elements of the system can be executed in the following ways, being at the root (following the guidelines of the statement, which are not specified here, only a guide with the default rules):
- Controller:
	```bash
	python3 -m controller.controller
	```

- IoT devices:
	```bash
	python3 -m iot.dummy-switch <id>
	python3 -m iot.dummy-sensor <id>
	python3 -m iot.dummy-clock <id>
	```

- Django project (being in `iot-manager`):
	```bash
	python3 manage.py runserver # You can specify port if needed
	```

> **IMPORTANT NOTE:**  
> By default, the host value is taken as the supposed Mosquitto server of the EPS; however, this is not functional. It is necessary to provide `--host localhost` or the default path where the Mosquitto server is running.

In addition to the default parameters, both IoT and the controller handle the `--debug` parameter (by default in `false`), which serves to show relevant messages.

In the provided Makefile, there are shortcuts (`controller`, `manager`) to launch the controller and the Django project, respectively. In addition, there are also two other utilities:
- `mosquitto`: creates a fully functional Eclipse Mosquitto container on localhost with its default port.
- `mosquitto-web-ui`: creates a container of `emqx/mqttx-web`, which offers a simple graphical interface to view messages from the topics of a specific system, perfect at the beginning to observe the behavior of IoT devices.

## Requirements
- Create, delete, edit and observe device information.
- Create, delete, edit and observe rule information.
- Create an interface for the user to interact with the system elements.
- Implement 3 types of devices (DummySwitch, DummySensor, DummyClock).
- Implement the system controller (and the Rule Engine separately if necessary).

## Decisions
- **Should Controller and Rule Engine be separate applications?, why?, what advantages does each option have?**  
	If done separately, the controller should only listen to devices, send information to the Rule Engine, listen from the Rule Engine and send data to the "commands" topics of the devices. However, we believe that the Rule Engine could be executed in the controller itself. In this way, we eliminate the step of maintaining a new connection. In addition, database accesses are optimized, so the time lost in our implementation is less than what would be lost with two independent entities.

- **How do Controller and Rule Engine communicate in the chosen option?**  
	Being both in the controller, the Rule Engine would be the thread that is created when receiving a message from the topic of some device.

- **Does it make sense for any of these components to share functionality?, what relationship is there between them?**  
	In our opinion, having them separate would be more difficult to handle. The controller should really be in charge of handling the entire system. Making it depend on an external unit could generate problems.

- **How many instances are there of each component?**  
	All components can be executed in multiple instances. The only requirement with IoT is that they have different IDs (in case of being launched by the user, in the Django project this is limited).

## Implementations
- The devices are specified in the document `doc/iots`.
- The controller is responsible for listening to the topics where IoT devices publish their states. At the moment a message arrives, it is checked if said device is found as the source device of some rule; if positive, it is checked if the state parameters match the comparisons and values that the rule is made of. If this is met, the message, also specified in the rule, is sent to the destination device.
- **Rule Engine:** As explained in the "Decisions" field, we have decided to implement it together with the controller, knowing what it entails.
- The Django project is responsible for presenting a pleasant interface in which a user can create, delete and edit devices and rules, along with a section to view the generated logs.

## Conclusions
We believe that, given the time dedicated and the time available for the project (we think more than two weeks would have been necessary, especially since we only had one class per week and all the deadlines were so soon), we have developed a solid and functional product, with a fairly simple and intuitive interface. The logging and visualization system allows users to clearly see which devices are running, as well as a list of all the rules currently being analyzed in the system.
