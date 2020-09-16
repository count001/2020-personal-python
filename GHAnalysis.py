import json
import os
import argparse

def	data(dict_address):
	Users = {}
	Repos = {}
	Users_Repos = {}
	json_list = []
	for root, dic, files in os.walk(dict_address):
		for f in files:
			if(f[-5:] == '.json'):
				x = open(dict_address + '\\' + f, 'r', encoding = 'utf-8').read()
				for i in x.split('\n'):
					if(len(i)>0):
						json_list.append(json.loads(i))
	for i in json_list:
		Type = i.get('type',0)
		User = i.get('actor',0).get('login',0)
		Repo = i.get('repo',0).get('name',0)

		if not Users.get(User):
			Users.update({User: {}})
		if not Users[User].get(Type):
			Users[User].update({Type: 0})
		Users[User][Type] += 1

		if not Repos.get(Repo):
			Repos.update({Repo: {}})
		if not Repos[Repo].get(Type):
			Repos[Repo].update({Type: 0})
		Repos[Repo][Type] += 1

		if not Users_Repos.get(User):
			Users_Repos.update({User: {}})
		if not Users_Repos[User].get(Repo):
			Users_Repos[User].update({Repo: {}})
		if not Users_Repos[User][Repo].get(Type):
			Users_Repos[User][Repo].update({Type: 0})
		Users_Repos[User][Repo][Type] += 1
	with open('Users.json', 'w', encoding='utf-8') as f:
		json.dump(Users,f)
	with open('Repos.json', 'w', encoding='utf-8') as f:
		json.dump(Repos,f)
	with open('Users_Repos.json', 'w', encoding='utf-8') as f:
		json.dump(Users_Repos,f)

def getEventsRepos(repo, event):
	x = open('Repos.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if not file.get(repo,0):
		print("0")
	else:
		print(file[repo].get(event,0))

def getEventsUsers(user, event):
	x = open('Users.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if not file.get(user,0):
		print("0")
	else:
		print(file[user].get(event,0))

def getEventsUsersAndRepos(user, repo, event):
	x = open('Users_Repos.json', 'r', encoding='utf-8').read()
	file = json.loads(x)
	if not file.get(user,0):
		print("0")
	elif not file[user].get(repo):
		print("0")
	else:
		print(file[user][repo].get(event,0))


class Run:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.argInit()
		self.analyse()

	def argInit(self):
		self.parser.add_argument('-i', '--init')
		self.parser.add_argument('-u', '--user')
		self.parser.add_argument('-r', '--repo')
		self.parser.add_argument('-e', '--event')

	def analyse(self):
		if(self.parser.parse_args().init):
			data(self.parser.parse_args().init)
			return 0
		else:
			if(self.parser.parse_args().event):
				if(self.parser.parse_args().user):
					if(self.parser.parse_args().repo):
						getEventsUsersAndRepos(
							self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
					else:
						getEventsUsers(
							self.parser.parse_args().user, self.parser.parse_args().event)
				elif (self.parser.parse_args().repo):
					getEventsRepos(
						self.parser.parse_args().reop, self.parser.parse_args().event)
				else:
					raise RuntimeError('error: argument -l or -c are required')
					return 0
			else:
				raise RuntimeError('error: argument -e is required')
				return 0

if __name__ == '__main__':
	a = Run()
