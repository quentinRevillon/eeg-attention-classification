# AIoT : Artifical Intelligence of Things.
#### EEG signals for attention and memory
.

## Summary
.
- Our Team
- Project description
- Usage
- Roadmap
- Credits

.
## Our Team

### Team attention
- Quentin REVILLION
- Charles KAYSSIEH
- Felicité YVERT
### Team memory
- Prisha CHADIRAMANI
- Manon STRASSER

.
## Project description
.

This project is about our profound desire to understand humans and the way they think. Using AI and ML, we aim at using the EEG signals of the brain to help users gain autonomy over their attention and memory capacities.

This project is the result of a collaboration between doctorants and our team of first year engineer students.

Our job was to develop web applications which will test the attention and memory of users. Then, while learning about tinyML, we gathered date during testing session with volontary people. Finally, we create a complete dataset of EEG files in order to train TinyML models.

.
## Usage
.
- **Web Applications** :
To launch the web applications home page, you should download the project on your computer, then type "python app.py" in the terminal while being in the right folder.

- **Testing session** :
You can find the protocole in the git project, in the main branch :[link here](https://gitlab.telecom-paris.fr/proj104/aiot/-/blob/main/Protocole.txt?ref_type=heads)
To register for the database, just use your email adress and a password.

.

## Roadmap for the Project

.

### Our part :

- **Research about attention and memory** :
We used the ressources given by the doctorants, in addition to personal reasearch approved by our supervisor.
- **Web Applications** :
Both team decided to implements games based on our research, using different languages (Java, React..). We also created a databas
to gather the results (the eeg files and the scores of the games)
- **Protocole** :
After meetings with the doctorant team, we worked on the protocoles, in order to produce consistent data between tests. It also should conform to the requirements of the psychological comitee (for the legal aspect of the projects outside ou our realm)
- **Gathering Data** :
On multiple session, we install the headset that measures the eeg signals of mutliple points on the crane (about 50 electrodes), which lasts for an hour, then we proceed with the protole which lasts for about 40 minutes.

.

### The rest of the project :
.

- **Clean the data** :
The doctorants worked on signal treatment (different types of transforms such as Fourrier Transform) in order for the models to learn things.

- **Choose a model to train** :
The team looked at different types of model that would be adapted to our Usage.

- **Implementation** :
_In fine_, the goal of the trained model is to be implemented in a small embeded device, wich should ressemble earphones. It should display in real time informations about the attention and memory levels of the wearer.

.

## Credits
.

We would like to thank our supervisor, **Van-Tam Nguyen**, which helped us navigate this complex project.

Thanks also to the doctorant team, composed of : Nasim, Remi, Aël, YingHao, namely, who helped answer our questions and provided support during the whole time of the project.

.