#!/usr/bin/python

from math import exp
from random import uniform
import json
rate = 0.25
dic = {}

def weighted_choice(somedict):
    n = uniform(0, 1)
    chsum = 0
    for dec in somedict:
        chsum = chsum+exp(somedict[dec])
    for dec in somedict:
        weight = exp(somedict[dec])/chsum
        if n < weight:
            break
        n = n - weight
    return dec

def reaction(ro, re):
    td = ro - re
    if td > 2:
        return "You should have enjoyed dinner tonight!"
    elif td < -2:
        return "Aww, I'm sorry. I'm sure you can get better food next time."
    else:
        return "So dinner was okay tonight, I guess?"

def ask_yn(prompt, default):
    while True:
        usr_inp = raw_input(prompt)
        if usr_inp == "":
            usr_inp = default
        if usr_inp.upper() == "Y":
            return True
        elif usr_inp.upper() == "N":
            return False
        else:
            print "Invalid option. Enter Y or N."

def save_dic(somedict):
    f = open(".restaurantdb", "w")
    f.write(json.dumps(dic))

def update_q(place_name):
    re = dic[place_name]
    ro = int(raw_input("On a scale of 0 to 9, how did you enjoy dinner? "))
    print reaction(ro, re)
    dic[place_name] = dic[place_name] + rate*(ro-re)
    save_dic(dic)

def new_place():
    new_name = raw_input("What's the place's name? ")
    dic[new_name] = 5
    update_q(new_name)

def choose_place():
    if len(dic) == 0:
        print "I'm sorry, I don't know the places you have been to."
    else:
        chosen_name = weighted_choice(dic)
        print "You should go to", chosen_name
        update_q(chosen_name)

def interactive():
    while True:
        if ask_yn("Do you want to go to a new place tonight (y/N): ", "N"):
            new_place()
        else:
            choose_place()
        print

print "Hi! Welcome to Dopamine, the intelligent restaurant chooser."
print "Press <C-d> at anytime to quit."
has_file = True
try:
    f = open(".restaurantdb", "r")
except IOError:
    has_file = False
    print "Creating restaurant database file .restaurantdb ..."
if has_file:
    inp_file = f.read()
    dic = json.loads(inp_file)
print
try:
    interactive()
except EOFError:
    print
    print "Bye!"
    exit()
