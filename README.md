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
- Prisha CHANDIRAMANI
- Manon STRASSER

.
## Project description
.

We chose this project based on our profound desire to understand humans and the way they think. Using AI and ML, we aim at using the EEG signals of the brain to help users gain autonomy over their attention and memory capacities.

This project is the result of a collaboration between doctorants and our team of first year engineer students.

Our job was to develop web applications which will test the attention and memory of users. Then, while learning about TinyML, we gathered data during testing sessions with volontary people. Finally, we created a complete dataset of EEG files in order to train TinyML models.

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
We used the ressources given by the doctorants, in addition to personal research approved by our supervisor.
- **Web Applications** :
Both team decided to implements games based on our research, using different languages (Java, React..). We also created a database to gather the results (the EEG files and the scores of the games).
- **Protocole** :
After meetings with the doctorant team, we worked on the protocoles, in order to produce consistent data between tests. It also should conform to the requirements of the psychological committee (for the legal aspect of the projects outside of our realm).
- **Gathering Data** :
On multiple sessions, we installed the helmet that measures the EEG signals of mutliple points on the head (about 84 electrodes). Each session lasts 1 hour 45 minutes. It takes one hour to set up the helmet and 40 minutes to complete the protocole.

.

### The rest of the project :
.

- **Clean the data** :
The doctorants worked on signal treatment (different types of transforms such as Fourrier Transform) in order for the models to learn things.
EEG signals contain a lot of noise that needs to be removed before using them as a data set. 

- **Choose a model to train** :
The team looked at different types of model that would be adapted to our usage.

- **Implementation** :
Ultimately, the goal of the trained model is to be implemented in a small embedded device, wich should resemble earphones. It should display real time information about the attention and memory levels of the wearer.

.

## Credits
.

We would like to thank our supervisor, **Van-Tam Nguyen**, which helped us navigate this complex project.

Thanks also to the doctorant team, composed of : Nasim Bagheri Shouraki, Remi Nahon, Aël Quélennec, YingHao Wang, who helped answer our questions and provided support during the whole time of the project.

.