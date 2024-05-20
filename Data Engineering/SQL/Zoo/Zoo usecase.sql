
#For the following usecase, I have asked chat gpt to create tables and data about a zoo and to propose some exercicies to explore the data. 
#The main idea of this script is to showcase my skills in SQL.


create database Zoo;
use Zoo;


#The following tables and data has been created by cat gpt:

CREATE TABLE Animals (
    AnimalID INT PRIMARY KEY,
    Name VARCHAR(100),
    SpeciesID INT,
    HabitatID INT,
    DateOfBirth DATE,
    Gender CHAR(1),
    FOREIGN KEY (SpeciesID) REFERENCES Species(SpeciesID),
    FOREIGN KEY (HabitatID) REFERENCES Habitats(HabitatID)
);

CREATE TABLE Species (
    SpeciesID INT PRIMARY KEY,
    CommonName VARCHAR(100),
    ScientificName VARCHAR(100),
    ConservationStatus VARCHAR(50)
);

CREATE TABLE Habitats (
    HabitatID INT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Location VARCHAR(100)
);

CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE,
    HireDate DATE,
    PersonalityID INT,
    FOREIGN KEY (PersonalityID) REFERENCES Personalities(PersonalityID)
);

CREATE TABLE Personalities (
    PersonalityID INT PRIMARY KEY,
    Trait VARCHAR(100),
    Description TEXT
);

CREATE TABLE Animal_Care (
    CareID INT PRIMARY KEY,
    AnimalID INT,
    EmployeeID INT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY,
    Name VARCHAR(100),
    Date DATE,
    Description TEXT,
    Location VARCHAR(100)
);

CREATE TABLE Animal_Events (
    AnimalEventID INT PRIMARY KEY,
    EventID INT,
    AnimalID INT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (AnimalID) REFERENCES Animals(AnimalID)
);

CREATE TABLE Employee_Skills (
    SkillID INT PRIMARY KEY,
    EmployeeID INT,
    Skill VARCHAR(100),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);



INSERT INTO Species (SpeciesID, CommonName, ScientificName, ConservationStatus)
VALUES 
(1, 'African Elephant', 'Loxodonta africana', 'Vulnerable'),
(2, 'Bengal Tiger', 'Panthera tigris tigris', 'Endangered'),
(3, 'King Cobra', 'Ophiophagus hannah', 'Vulnerable'),
(4, 'Giant Panda', 'Ailuropoda melanoleuca', 'Vulnerable'),
(5, 'Komodo Dragon', 'Varanus komodoensis', 'Vulnerable'),
(6, 'Harpy Eagle', 'Harpia harpyja', 'Near Threatened'),
(7, 'Red Kangaroo', 'Macropus rufus', 'Least Concern'),
(8, 'Snow Leopard', 'Panthera uncia', 'Vulnerable'),
(9, 'Blue Poison Dart Frog', 'Dendrobates tinctorius', 'Least Concern'),
(10, 'Galapagos Tortoise', 'Chelonoidis nigra', 'Vulnerable'),
(11, 'Chimpanzee', 'Pan troglodytes', 'Endangered'),
(12, 'Great White Shark', 'Carcharodon carcharias', 'Vulnerable'),
(13, 'Polar Bear', 'Ursus maritimus', 'Vulnerable'),
(14, 'Scarlet Macaw', 'Ara macao', 'Least Concern'),
(15, 'African Lion', 'Panthera leo', 'Vulnerable');

INSERT INTO Habitats (HabitatID, Name, Description, Location)
VALUES 
(1, 'Savannah', 'Large open grasslands with scattered trees', 'North Section'),
(2, 'Jungle', 'Dense forest with high humidity', 'East Section'),
(3, 'Desert', 'Hot, arid area with sparse vegetation', 'South Section'),
(4, 'Mountain', 'Rocky area with high elevation and cool temperatures', 'West Section'),
(5, 'Rainforest', 'Dense, tropical forest with high rainfall', 'Central Section'),
(6, 'Wetlands', 'Area with marshes and swamps', 'North-East Section'),
(7, 'Riverbank', 'Area along the river with lush vegetation', 'East-Central Section'),
(8, 'Coastal', 'Area along the coast with sandy beaches and ocean access', 'South-West Section'),
(9, 'Arctic', 'Cold, icy area with minimal vegetation', 'North-West Section'),
(10, 'Aquarium', 'Enclosed water habitats for marine animals', 'Central-West Section');

INSERT INTO Personalities (PersonalityID, Trait, Description)
VALUES 
(1, 'Jovial', 'Always cheerful and good-humored'),
(2, 'Serious', 'Takes things very seriously and is very focused'),
(3, 'Energetic', 'Full of energy and always active'),
(4, 'Calm', 'Relaxed and composed, rarely gets flustered'),
(5, 'Curious', 'Always eager to learn new things and explore'),
(6, 'Organized', 'Keeps everything in order and is very methodical'),
(7, 'Empathetic', 'Able to understand and share the feelings of others'),
(8, 'Witty', 'Quick and inventive verbal humor'),
(9, 'Adventurous', 'Willing to take risks and try new experiences'),
(10, 'Patient', 'Able to wait without becoming annoyed or anxious'),
(11, 'Observant', 'Pays close attention to details'),
(12, 'Innovative', 'Introduces new ideas and methods'),
(13, 'Gentle', 'Kind and tender-hearted'),
(14, 'Assertive', 'Confident and forceful'),
(15, 'Resourceful', 'Able to deal with new or difficult situations effectively');

INSERT INTO Employees (EmployeeID, FirstName, LastName, DateOfBirth, HireDate, PersonalityID)
VALUES 
(1, 'Alice', 'Smith', '1985-06-15', '2010-03-01', 1),
(2, 'Bob', 'Johnson', '1990-12-20', '2015-07-22', 2),
(3, 'Charlie', 'Brown', '1978-04-10', '2005-11-30', 3),
(4, 'Daisy', 'Miller', '1988-08-25', '2012-08-01', 4),
(5, 'Ethan', 'Jones', '1992-03-05', '2018-05-15', 5),
(6, 'Fiona', 'Davis', '1983-11-14', '2009-02-20', 6),
(7, 'George', 'Clark', '1975-01-22', '2000-10-10', 7),
(8, 'Hannah', 'Lewis', '1989-07-30', '2011-06-17', 8),
(9, 'Ian', 'Walker', '1995-09-12', '2020-01-10', 9),
(10, 'Jenny', 'Hall', '1987-05-18', '2014-09-25', 10),
(11, 'Kevin', 'Martinez', '1986-04-22', '2011-11-01', 11),
(12, 'Laura', 'Garcia', '1991-02-14', '2017-08-05', 12),
(13, 'Michael', 'Williams', '1980-01-09', '2007-07-19', 13),
(14, 'Nancy', 'Brown', '1984-10-25', '2010-12-05', 14),
(15, 'Oscar', 'Wilson', '1993-06-11', '2019-03-22', 15);

INSERT INTO Animals (AnimalID, Name, SpeciesID, HabitatID, DateOfBirth, Gender)
VALUES 
(1, 'Dumbo', 1, 1, '2012-04-12', 'M'),
(2, 'Sheru', 2, 2, '2014-09-21', 'F'),
(3, 'Nagini', 3, 2, '2016-11-03', 'M'),
(4, 'Bamboo', 4, 5, '2010-05-28', 'F'),
(5, 'Draco', 5, 3, '2013-03-15', 'M'),
(6, 'Harpy', 6, 4, '2011-02-10', 'F'),
(7, 'Roo', 7, 1, '2015-07-19', 'M'),
(8, 'Snowy', 8, 4, '2017-12-22', 'F'),
(9, 'Bluey', 9, 6, '2019-08-30', 'M'),
(10, 'Tortie', 10, 7, '2009-09-09', 'F'),
(11, 'Chimpy', 11, 5, '2013-05-05', 'M'),
(12, 'Whitey', 12, 10, '2014-06-11', 'F'),
(13, 'Polar', 13, 9, '2012-01-29', 'M'),
(14, 'Scarlet', 14, 5, '2011-08-12', 'F'),
(15, 'Simba', 15, 1, '2016-03-22', 'M'),
(16, 'Luna', 4, 5, '2018-11-25', 'F'),
(17, 'Sandy', 3, 3, '2015-09-17', 'F'),
(18, 'Rex', 7, 1, '2017-12-04', 'M'),
(19, 'Leo', 15, 1, '2019-05-20', 'M'),
(20, 'Blaze', 8, 4, '2015-10-13', 'M');

INSERT INTO Animal_Care (CareID, AnimalID, EmployeeID, StartDate, EndDate)
VALUES 
(1, 1, 1, '2015-01-01', NULL),
(2, 2, 2, '2016-05-15', NULL),
(3, 3, 3, '2017-03-22', NULL),
(4, 4, 4, '2018-07-30', NULL),
(5, 5, 5, '2019-10-05', NULL),
(6, 6, 6, '2020-12-18', NULL),
(7, 7, 7, '2021-04-12', NULL),
(8, 8, 8, '2022-09-01', NULL),
(9, 9, 9, '2023-01-15', NULL),
(10, 10, 10, '2023-05-23', NULL),
(11, 11, 11, '2015-01-01', '2016-12-31'),
(12, 12, 12, '2017-01-01', '2018-12-31'),
(13, 13, 13, '2019-01-01', '2020-12-31'),
(14, 14, 14, '2021-01-01', NULL),
(15, 15, 15, '2022-01-01', NULL),
(16, 16, 1, '2021-01-01', '2022-12-31'),
(17, 17, 2, '2021-01-01', '2022-12-31'),
(18, 18, 3, '2021-01-01', '2022-12-31'),
(19, 19, 4, '2021-01-01', '2022-12-31'),
(20, 20, 5, '2021-01-01', '2022-12-31');

INSERT INTO Events (EventID, Name, Date, Description, Location)
VALUES 
(1, 'Elephant Parade', '2023-06-01', 'Parade of elephants across the zoo', 'Main Pathway'),
(2, 'Tiger Talk', '2023-07-15', 'Interactive session about tigers', 'Jungle Habitat'),
(3, 'Reptile Show', '2023-08-10', 'Display of various reptiles', 'Reptile House'),
(4, 'Panda Picnic', '2023-09-05', 'Watch pandas during their feeding time', 'Panda Habitat'),
(5, 'Eagle Flight', '2023-10-20', 'Demonstration of eagle flight and hunting', 'Mountain Habitat'),
(6, 'Kangaroo Jump', '2023-11-25', 'Showcase of kangaroo agility and jumping', 'Savannah'),
(7, 'Snow Leopard Tracking', '2023-12-15', 'Learn about tracking snow leopards', 'Mountain Habitat'),
(8, 'Frog Fest', '2024-01-18', 'Exhibit of various frog species', 'Wetlands'),
(9, 'Tortoise Trek', '2024-02-22', 'Observe the movements of giant tortoises', 'Riverbank'),
(10, 'Dragon Tales', '2024-03-30', 'Stories and facts about Komodo dragons', 'Desert'),
(11, 'Chimpanzee Chat', '2024-04-12', 'Learn about the life of chimpanzees', 'Rainforest'),
(12, 'Shark Dive', '2024-05-15', 'Observe great white sharks in action', 'Aquarium'),
(13, 'Polar Bear Plunge', '2024-06-20', 'Watch polar bears swim and play', 'Arctic'),
(14, 'Macaw Magic', '2024-07-25', 'Interactive session with scarlet macaws', 'Rainforest'),
(15, 'Lion King', '2024-08-30', 'Learn about the life of African lions', 'Savannah');

INSERT INTO Animal_Events (AnimalEventID, EventID, AnimalID)
VALUES 
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 6),
(6, 6, 7),
(7, 7, 8),
(8, 8, 9),
(9, 9, 10),
(10, 10, 5),
(11, 11, 11),
(12, 12, 12),
(13, 13, 13),
(14, 14, 14),
(15, 15, 15),
(16, 1, 16),
(17, 2, 17),
(18, 3, 18),
(19, 4, 19),
(20, 5, 20);

INSERT INTO Employee_Skills (SkillID, EmployeeID, Skill)
VALUES 
(1, 1, 'Elephant Handling'),
(2, 2, 'Tiger Training'),
(3, 3, 'Reptile Care'),
(4, 4, 'Panda Management'),
(5, 5, 'Komodo Dragon Expertise'),
(6, 6, 'Eagle Training'),
(7, 7, 'Kangaroo Care'),
(8, 8, 'Snow Leopard Research'),
(9, 9, 'Frog Care'),
(10, 10, 'Tortoise Handling'),
(11, 11, 'Chimpanzee Interaction'),
(12, 12, 'Shark Care'),
(13, 13, 'Polar Bear Care'),
(14, 14, 'Macaw Interaction'),
(15, 15, 'Lion Care'),
(16, 1, 'General Animal Care'),
(17, 2, 'Environmental Enrichment'),
(18, 3, 'Medical Treatment'),
(19, 4, 'Dietary Planning'),
(20, 5, 'Behavioral Observation');




#THE FOLLOWING CODE IS THE ONE THAT I DEVELOPED FOLLOWING THE TASKS THAT CHAT GPT HAS PROPOSED:

#List all animal names and their species.
SELECT Animals.Name, Species.CommonName
FROM Animals
LEFT JOIN Species on Animals.SpeciesID= Species.SpeciesID;


#Find the names and hire dates of all employees.
SELECT FirstName, LastName, HireDate from Employees;


#List all animals born after January 1, 2015.
SELECT Name, DateOfBirth from Animals;


#Find all employees with the personality trait "Jovial".
SELECT Employees.FirstName
FROM Employees
LEFT JOIN Personalities on Employees.PersonalityID= Personalities.PersonalityID
WHERE Personalities.Trait ="Jovial";


#Count the number of animals in each habitat.
SELECT Habitats.Name, count(Animals.Name)
FROM Habitats
LEFT JOIN Animals ON Habitats.HabitatID=Animals.HabitatID
GROUP BY Habitats.Name;


#Find the average age of employees.
SELECT avg(TIMESTAMPDIFF(YEAR, Employees.DateOfBirth, NOW())) AS average_age
FROM Employees;


#List all events and the animals involved in them.
SELECT Events.Name, Animals.Name
FROM Events
JOIN Animal_Events ON Events.EventID=Animal_Events.EventID
LEFT JOIN Animals ON Animal_Events.AnimalID=Animals.AnimalID;


#Find all employees and the animals they are currently taking care of.
SELECT Employees.FirstName, Animals.Name
FROM Employees
JOIN Animal_Care ON Employees.EmployeeID=Animal_Care.EmployeeID
LEFT JOIN Animals ON Animal_Care.AnimalID=Animals.AnimalID;


#Find employees who have taken care of more than 1 different animal.
SELECT concat(Employees.FirstName," ", Employees.LastName) as name, count(Animals.Name) as Animals_take_care
FROM Employees
JOIN Animal_Care ON Employees.EmployeeID=Animal_Care.EmployeeID
LEFT JOIN Animals ON Animal_Care.AnimalID=Animals.AnimalID
GROUP BY concat(Employees.FirstName," ", Employees.LastName)
HAVING Animals_take_care>1;


#List the habitats that have more than one type of species.
SELECT Habitats.Name, COUNT(Species.CommonName)
FROM Habitats
JOIN Animals ON Habitats.HabitatID=Animals.HabitatID
JOIN Species ON Animals.SpeciesID=Species.SpeciesID
GROUP BY Habitats.Name
HAVING COUNT(Species.CommonName) >1;


#Find the total number of events each animal has participated in and list them in descending order.
SELECT Animals.Name, count(Events.Name)
FROM Animals
JOIN Animal_Events ON Animals.AnimalID = Animal_Events.AnimalID
LEFT JOIN Events ON Animal_Events.EventID= Events.EventID
GROUP BY Animals.Name
ORDER BY Animals.Name DESC;


#List the names of animals and their caretakers where the caretaker has a personality trait of "Empathetic".
SELECT Animals.Name
FROM Animals
JOIN Animal_Care ON Animals.AnimalID=Animal_Care.AnimalID
LEFT JOIN Employees ON  Animal_Care.EmployeeID=Employees.EmployeeID
LEFT JOIN Personalities ON Employees.PersonalityID=Personalities.PersonalityID
WHERE Personalities.Trait = "Empathetic";


#Find the top 3 employees who have taken care of the most animals. Display their names, the number of animals they have taken care of, and list the names of the animals.
SELECT concat(Employees.FirstName," ", Employees.LastName) , count(Animals.Name) 
FROM Employees
JOIN Animal_Care ON Employees.EmployeeID=Animal_Care.EmployeeID
LEFT JOIN Animals ON Animal_Care.AnimalID=Animals.AnimalID
GROUP BY concat(Employees.FirstName," ", Employees.LastName)
ORDER BY count(Animals.Name) DESC
LIMIT 3;


#For each species, find the average age of the animals and display the species name, average age, and the number of animals in that species.
SELECT Species.CommonName, AVG(TIMESTAMPDIFF(YEAR, Animals.DateOfBirth, NOW())), count(Animals.Name)
FROM Species
LEFT JOIN Animals ON Species.SpeciesID = Animals.SpeciesID
GROUP BY Species.CommonName;


#Find the animal that has participated in the most events. Display the animal's name, species, and the number of events they have participated in.
SELECT Animals.Name, Species.CommonName, count(Events.Name)
FROM Animals
LEFT JOIN Species ON Animals.SpeciesID=Species.SpeciesID
LEFT JOIN Animal_Events on Animals.AnimalID = Animal_Events.AnimalID
LEFT JOIN Events ON Animal_Events.EventID=Events.EventID
GROUP BY Animals.Name, Species.CommonName
ORDER BY count(Events.Name) DESC
LIMIT 1;
 

#List all employees along with the total number of animals they are currently taking care of, and rank them based on this number using window functions.
SELECT Employees.FirstName , count(Animal_Care.AnimalID), RANK() OVER (ORDER BY COUNT(Animal_Care.AnimalID) DESC) AS Rank_Animal
FROM Employees
LEFT JOIN Animal_Care ON Employees.EmployeeID = Animal_Care.EmployeeID
WHERE Animal_Care.EndDate IS NULL
GROUP BY Employees.FirstName;


#Update the conservation status of the "Bengal Tiger" to "Critically Endangered".
UPDATE Species
SET ConservationStatus = 'Critically Endangered'
WHERE CommonName = 'Bengal Tiger';


#Update the habitat of all animals that are currently taken care of by an employee with the personality trait "Adventurous" to a new habitat called 'North Section'.
UPDATE Animals
SET HabitatID = (SELECT HabitatID FROM Habitats WHERE Location = 'North Section') #1
WHERE AnimalID IN (SELECT Animal_Care.AnimalID
    FROM Animal_Care 
    JOIN Employees  ON Animal_Care.EmployeeID = Employees.EmployeeID
    WHERE Employees.PersonalityID = (SELECT PersonalityID
FROM Personalities
WHERE Trait = 'Adventurous') #9
AND Animal_Care.EndDate IS NULL
);


#Remove all animal care records for animals that are no longer in the zoo (e.g., those with NULL habitat).
DELETE FROM Animal_Care
WHERE AnimalID IN (
    SELECT AnimalID
    FROM Animals
    WHERE HabitatID IS NULL
);
