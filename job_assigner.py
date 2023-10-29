from typing import List
import random
import pandas as pd
import sys
import json

num_slots_per_job = 2

class Job:

    def __init__(self, name:str) -> None:
        self.name = name
        self.num_slots = num_slots_per_job
        self.num_assigned = 0
    
    def get_name(self) -> str:
        return self.name
    
    def is_filled(self) -> bool:
        return self.num_assigned == self.num_slots
    
    def assign(self) -> None:
        self.num_assigned += 1
    
    def unassign(self) -> None:
        self.num_assigned -= 1

class Person:

    def __init__(self, id:int, first_name:str, last_name:str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.assigned_job = None
        self.previous_jobs = []

    def get_first_name(self) -> str:
        return self.first_name
    
    def get_last_name(self) -> str:
        return self.last_name
    
    def get_id(self) -> str:
        return self.id
    
    def get_assigned_job(self) -> Job:
        return self.assigned_job
    
    def get_previous_jobs(self) -> List[str]:
        job_names = []
        for job in self.previous_jobs:
            job_names.append(job.get_name)
        return job_names
    
    def assign_job(self, job:Job) -> None:
        if self.assigned_job:
            self.previous_jobs.append(self.assigned_job)
            self.assigned_job.unassign()
        self.assigned_job = job
        job.assign()

    def reset_jobs(self) -> None:
        self.assigned_job = None
        self.previous_jobs = []

class JobAssigner:

    def __init__(self) -> None:
        self.people = []
        self.jobs = []

    def get_num_available_jobs(self) -> int:
        return len(self.jobs)
    
    def get_num_people(self) -> int:
        return len(self.people)
    
    def get_people(self) -> List[Person]:
        return self.people
    
    def get_jobs(self) -> List[Job]:
        return self.jobs
    
    def add_person(self, person:Person) -> None:
        self.people.append(person)
    
    def add_job(self, job:Job) -> None:
        if job not in self.jobs:
            self.jobs.append(job)

    def get_random_available_job(self) -> Job:
        """
        finds the next available random job
        """
        index = random.randint(0, self.get_num_available_jobs() - 1)
        job = self.jobs[index]
        while job.is_filled():
            index += 1
            if index >= len(self.jobs):
                index = 0
            job = self.jobs[index]
        
        return job
    
    def random_assign(self) -> None:
        """
        REQUIRES: there are at least as many jobs as people
        """
        if len(self.people) > len(self.jobs) * num_slots_per_job:
            raise Exception("Not enough jobs")
        else: 
            for person in self.people:
                job = self.get_random_available_job()
                while job.get_name() in person.get_previous_jobs():
                    job = self.get_random_available_job()
                person.assign_job(job)

    def reset_jobs(self) -> None:
        for person in self.people:
            person.reset_jobs()

    def to_json(self) -> None:
        json_dump = json.dumps(self.__dict__)
        print(json_dump)
        with open("data.json", "w") as outfile:
            outfile.write(json_dump)

    def read_json(self) -> None:
        try: 
            file = open("data.json")
            #TODO: read python class object
        except: 
            print("File not found.")

if __name__ == "__main__":
    
    job_assigner = JobAssigner()

    print("Welcome to Job Assigner")
    print("Would you like to create a new assignment list?")
    response = -1
    while response not in [1, 2]:
        print("[1] continue with previous")
        print("[2] start a new one")
        response = int(input("Enter your value: "))
        if response not in [1, 2]:
            print("Invalid choice, try again.")
    
    if response == 1:
        #TODO: read from JSON, run random_assign(), if len(previous_jobs) == len(jobs) then reset
        pass
    else: 
        file_path = str(input("Enter the file path of your excel file containing jobs: "))

        data = pd.read_excel(file_path, header=None)
        print(data)

        jobs = data.iloc[:,0].tolist()
        print(jobs)
        num_people = sys.maxsize
        num_people = int(input("Enter the number of people: "))
        while num_people > len(jobs) * num_slots_per_job:
            print("Enter a number less than ", len(jobs) * num_slots_per_job)
            num_people = int(input("Enter the number of people: "))

        for job_name in jobs:
            job_assigner.add_job(Job(job_name))

        for i in range(1, num_people):
            print(i)
            person = Person(i, "first name", "last name")
            print(person.get_id())
            job_assigner.add_person(person) # placeholder names, none taken currently

        print(len(job_assigner.get_people()))
        print(len(job_assigner.get_jobs()))

        job_assigner.random_assign()
            
        out_data = {
            "person_id": [person.get_id() for person in job_assigner.get_people()],
            "job": [person.get_assigned_job().get_name() for person in job_assigner.get_people()],
        }

        pd.DataFrame(out_data).to_csv("out_data/job_assignments.csv")
        #job_assigner.to_json()
        print("All done!")
        