import sys
import random
from random import randrange
import time
from time import sleep

# Global variables
health = 0
max_health = 0
strength = 0
defense = 0
weapon_attack = 0
attack = 0
armor_defense = 0
shield = 0
exp = 0
inventory = []
level = 0
weapon = "None!"
armor = "None!"
monster = "None!"
monster_health = 0
monster_attack = 0
monster_shield = 0
monster_list = ["Goblin"]
monster_damage = 0
player_damage = 0


# Creates character stats at start or to reset stats
def char_stats(func):
	global health, max_health, strength, defense, weapon_attack, armor_defense, exp, weapon, armor, attack, shield, level, inventory
	
	if func == "start":
		level = 0
		exp = 0
		health = 150
		max_health = 150
		strength = random.randint(25, 35)
		defense = random.randint(25, 35)
		weapon_attack = random.randint(10, 20)
		armor_defense = random.randint(10, 20)
		inventory.append("potion")
		inventory.append("potion")
		weapon = "Bronze"
		armor = "Bronze"
		attack_and_shield_stats()
		print_slowly( """
Your starting stats are....\nLevel: %r\nHealth: %r/%r\nExperience: %r\nStrength: %r \nDefense: %r\nPotions: %r\nWeapon: %r\nWeapon Attack: %r\nArmor: %r\nArmor Defense: %r\nAttack: %r\nShield: %r\n\n""" % (level, health, max_health, exp, strength, defense, inventory.count("potion"), weapon, weapon_attack, armor, armor_defense, attack, shield))
		return level, health, max_health, strength, defense, weapon_attack, armor_defense, exp, weapon, armor, attack, shield
		
	elif func == "reset":
		health = 0
		max_health = 0
		strength = 0
		defense = 0
		weapon_attack = 0
		attack = 0
		armor_defense = 0
		shield = 0
		exp = 0
		level = 0
		weapon = "None!"
		armor = "None!"
		monster = "None!"
		monster_health = 0
		monster_attack = 0
		monster_shield = 0
		monster_list = ["Goblin"]
		monster_damage = 0
		player_damage = 0
		del inventory 
		inventory = []
		return health, max_health, strength, defense, weapon_attack, armor_defense, exp, weapon, armor, attack, shield, level, inventory
		
	elif func == "current":
		print_slowly( """
Your current stats are....\nLevel: %r\nHealth: %r/%r\nExperience: %r\nStrength: %r\nDefense: %r\nPotions: %r\nWeapon: %r\nWeapon Attack: %r\nArmor: %r\nArmor Defense: %r\nAttack: %r\nShield: %r""" % (level, health, max_health, exp, strength, defense, inventory.count("potion"), weapon, weapon_attack, armor, armor_defense, attack, shield))

# Calculates the attack and shield stats for battles from the current armor/character stats
def attack_and_shield_stats():
	global attack, shield, strength, defense, weapon_attack, armor_defense
	attack = ((strength * 2) + weapon_attack) / 2
	shield = ((defense * 2) + armor_defense) / 2
	return attack, shield

# Healing function, checks for potions, heals depending on if you have any potions and your current health, adjusts inventory
def heal(func):
	global health, max_health
	health_ratio = max_health - health
	sleep(1)
	if func == "potion":
		if "potion" in inventory and health_ratio > 100:
			print_slowly("\nYou use a potion and heal by 100.")
			inventory.remove("potion")
			health += 100
			print_slowly("\nYour health is %r/%r" % (health, max_health))
			return health
		elif "potion" in inventory and health_ratio < 100:
			print_slowly("\nYou use a potion to heal by %r." % health_ratio)
			inventory.remove("potion")
			health += health_ratio
			print_slowly("\nYour health is %r/%r" % (health, max_health))
			return health
		else:
			print_slowly("\nYou have no more Potions!")
	elif func == "big potion":
		if "big potion" in inventory and health_ratio > 250:
			print_slowly("\nYou use a big potion and heal by 100.")
			inventory.remove("big potion")
			health += 250
			print_slowly("\nYour health is %r/%r" % (health, max_health))
			return health
		elif "big potion" in inventory and health_ratio < 250:
			print_slowly("\nYou use a big potion to heal by %r." % health_ratio)
			inventory.remove("big potion")
			health += health_ratio
			print_slowly("\nYour health is %r/%r" % (health, max_health))
			return health
		else:
			print_slowly("\nYou have no more big potions!")
	elif func == "level":
		health = max_health
		print_slowly( "\nYou are healed!\n")
		return health
	elif func == "sleep":
		sleep(1)
		health = max_health
		print_slowly("\nAfter a night of rest your journey continues.\n")
		return health
		

# Used at the end of battles to add a prize to the inventory, most often a potion
def prize(what):
	sleep(1)
	if what == "Tissue":
		inventory.append("Tissue")
		print_slowly("\nYou got a tissue!!")
	elif what == "potion":
		inventory.append("potion")
		print_slowly("\nYou recieved a potion!")
	elif what == "big potion":
		inventory.append("big potion")
		print_slowly("\nYou recieved a big potion!")
	elif what == "Dragon Scale":
		inventory.append("Dragon Scale")
		print_slowly("\nYou recieved a Dragon Scale as a sign of the Dragon's allegance to you!")
	elif what == "Wolf Fang":
		inventory.append("Wolf Fang")
		print_slowly("\nYou recieved a Wolf Fang as a sign of the Wolf's allegance to you!")
	elif what == "Horse Shoe":
		inventory.append("Horse Shoe")
		print_slowly("\nYou recieved a Horse Shoe as a sign of the plainsmens allegiance to you!")
	else:
		print_slowly("\nIs that it?")
		print_slowly(what)

# Experience engine, run at the end of each battle, should add exp, adjust the characters stats, level, attack and shield if enough exp is earned.
def experience(gained):
	global exp, strength, defense, max_health, health, level
	exp = exp + gained
	if exp > 1000 and level == 5:
		exp = 1000
		print_slowly("\n\n**Your at max level!!**\n\n")
		char_stats("current")
	else:
		if exp in range(0, 101) and level == 0:
			attack_and_shield_stats()
			print_slowly("\n\nYou gained %r experience!\nYou are still Level 0. Get training!\n\n" % gained)
			return exp, strength, defense, max_health
		elif exp in range(101, 251) and level == 0:
			strength += 10
			defense += 10
			max_health += 25
			level += 1
			health = max_health
			attack_and_shield_stats()
			print_slowly("\n\nYou gained %r experience!\n**You reached Level 1!**\n\n" % gained)
			heal("level")
			char_stats("current")
			return exp, strength, defense, max_health, health, level
		elif exp in range(101, 251) and level == 1:
			print_slowly( "\n\nYou gained %r experience!\n" % gained)
		elif exp in range(251, 451) and level == 1:
			strength += 15
			defense += 15
			max_health += 25
			level += 1
			health = max_health
			attack_and_shield_stats()
			print_slowly("\n\nYou gained %r experience!\n**You reached Level 2!**\n\n" % gained)
			heal("level")
			char_stats("current")
			return exp, strength, defense, max_health, health, level
		elif exp in range(251, 451) and level == 2:
			print_slowly("\n\nYou gained %r experience!\n" % gained)
		elif exp in range(451, 701) and level == 2:
			strength += 20
			defense += 20
			max_health += 50
			level += 1
			health = max_health
			attack_and_shield_stats()
			print_slowly("\n\nYou gained %r experience!\n**You reached Level 3!**\n\n" % gained)
			heal("level")
			char_stats("current")
			return exp, strength, defense, max_health, health, level
		elif exp in range(451, 701) and level == 3:
			print_slowly( "\n\nYou gained %r experience!\n" % gained)
		elif exp in range(701, 999) and level == 3:
			strength += 25
			defense += 25
			max_health += 50
			level += 1
			health = max_health
			attack_and_shield_stats()
			print_slowly("\n\nYou gained %r experience!\n\t**You reached Level 4!**\n\n" % gained)
			heal("level")
			char_stats("current")
			return exp, strength, defense, max_health, health, level
		elif exp in range(701, 1000) and level == 4:
			print_slowly( "\n\nYou gained %r experience!\n" % gained)
		elif exp in range(1001, 1100) and level == 4:
			strength += 30
			defense += 30
			max_health += 50
			level += 1
			health = max_health
			attack_and_shield_stats()
			print_slowly("\n\n**You reached Level 5! Maximum Level!!**\n\n")
			heal("level")
			exp = 1000
			char_stats("current")
			return exp, strength, defense, max_health, health, level

# New weapon armor choice after the dragon battle.  Provides you with a new armor set, a new sword, and some better stats.  	
def weapon_armor_choice():
	global armor, weapon, weapon_attack, armor_defense, attack, shield
	sleep(1)
	found = random.randint(0,100)
	if found in range(0, 33):
		print_slowly("\n\nYou picked up a Steel armor set!")
		print_slowly("\nYou picked up a Steel sword!\n")
		armor = "Steel"
		weapon = "Steel"
		weapon_attack = random.randint(30, 45)
		armor_defense = random.randint(30, 45)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense, armor, weapon
	elif found in range(34, 66):
		print_slowly("\n\nYou picked up a Silver armor set!")
		print_slowly("\nYou picked up a Silver sword!\n")
		weapon = "Silver"
		armor = "Silver"
		weapon_attack = random.randint(55, 70)
		armor_defense = random.randint(55, 70)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense, armor, weapon
	elif found in range(67, 100):
		print_slowly("\n\nYou picked up a Gold armor set!")
		print_slowly("\nYou picked up a Gold sword!\n")
		weapon = "Gold"
		armor = "Gold"
		weapon_attack = random.randint(80, 95)
		armor_defense = random.randint(80, 95)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense, armor, weapon

# Weapon/Armor enhancement. Small guessing dialogue where you pick a number and it gets compared to a random number, the closer you are the better the enhancement,  should usually only provide slightly better stats.
def weapon_armor_enhance():
	global weapon_attack, armor_defense, attack, sheild
	print_slowly( """
Pick a number between 0 and 100. The closer you are to my number the better your armor will get!""")
	guessing = raw_input("\n> ")
	guess = int(guessing)
	answer = random.randint(0, 100)
	sleep(1)
	if guess > answer:
		difference = guess - answer
	else:
		difference = answer - guess
	if difference in range(1, 18):
		weapon_attack += 25
		armor_defense += 25		
		print_slowly("""
Great job! The difference was only %r! Your armor and sword are given great treatment! 
A magical glow surrounds your sword and armor, as the glow reaches its peak there is a bright flash! There is scroll work all over your armor and your sword seems lighter then ever.""" % difference)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense
	elif difference in range(19, 55):
		weapon_attack += 10
		armor_defense += 10
		print_slowly( """
Not bad! The difference was %r. With some refreshing your armor and sword gain power!""" % difference)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense
	elif difference in range(56,100):
		weapon_attack += 1
		armor_defense += 1
		print_slowly("""
What can I say... I've seen worse? We will give you an extra point of attack and shield as condolences on your guessing abilities. The difference was %r.""" % difference)
		attack_and_shield_stats()
		char_stats("current")
		return weapon_attack, armor_defense
	else:
		print_slowly("I don't think that's a number.")
		weapon_armor_enhance()

# Below are three random enemy "loads".  They are chosen during each segment of your travels at random by the the random_battle_decider.  These just set the monster stats and give you the proper prize if you won. The monster stats are increased with your level. : )
def random_enemy_one(func):
	global monster, monster_health, monster_attack, monster_shield, level
	which_prize = random.randint(0,100)
	if which_prize in range(0,51):
		winnings = "Tissue"
	else:
		winnings = "potion"
	if func == "stats" and level == 0:
		monster = "Goblin"
		monster_health = 100
		monster_attack = 45
		monster_shield = 55
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 1:
		monster = "Goblin"
		monster_health = 125
		monster_attack = 55
		monster_shield = 65
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 2:
		monster = "Goblin"
		monster_health = 150
		monster_attack = 60
		monster_shield = 80
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 3:
		monster = "Goblin"
		monster_health = 175
		monster_attack = 80
		monster_shield = 100
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 4:
		monster = "Goblin"
		monster_health = 200
		monster_attack = 105
		monster_shield = 125
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 5:
		monster = "Goblin"
		monster_health = 225
		monster_attack = 130
		monster_shield = 155
		return monster, monster_health, monster_attack, monster_shield
	elif func == "win" and level == 0:
		prize(winnings)
		experience(25)
	elif func == "win" and level == 1:
		prize(winnings)
		experience(30)
	elif func == "win" and level == 2:
		prize(winnings)
		experience(35)
	elif func == "win" and level == 3:
		prize(winnings)
		experience(40)
	elif func == "win" and level == 4:
		prize(winnings)
		experience(45)
	elif func == "win" and level == 5:
		prize(winnings)
		experience(50)
	else:
		print "Sorry I can't do that."

def random_enemy_two(func):
	global monster, monster_health, monster_attack, monster_shield
	if func == "stats":
		monster = "Troll"
		monster_health = 150
		monster_attack = 65
		monster_shield = 75
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 1:
		monster = "Troll"
		monster_health = 200
		monster_attack = 80
		monster_shield = 90
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 2:
		monster = "Troll"
		monster_health = 250
		monster_attack = 100
		monster_shield = 110
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 3:
		monster = "Troll"
		monster_health = 300
		monster_attack = 125
		monster_shield = 135
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 4:
		monster = "Troll"
		monster_health = 350
		monster_attack = 155
		monster_shield = 165
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 5:
		monster = "Troll"
		monster_health = 400
		monster_attack = 190
		monster_shield = 200
		return monster, monster_health, monster_attack, monster_shield
	elif func == "win" and level == 0:
		prize("potion")
		experience(40)
	elif func == "win" and level == 1:
		prize("potion")
		experience(50)
	elif func == "win" and level == 2:
		prize("big potion")
		experience(60)
	elif func == "win" and level == 3:
		prize("big potion")
		experience(70)
	elif func == "win" and level == 4:
		prize("big potion")
		experience(80)
	elif func == "win" and level == 5:
		prize("big potion")
		experience(95)
	else:
		print "Sorry I can't do that."
	
def random_enemy_three(func):
	global monster, monster_health, monster_attack, monster_shield
	if func == "stats":
		monster = "Rogue"
		monster_health = 200
		monster_attack = 75
		monster_shield = 75
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 1:
		monster = "Rogue"
		monster_health = 225
		monster_attack = 85
		monster_shield = 85
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 2:
		monster = "Rogue"
		monster_health = 250
		monster_attack = 100
		monster_shield = 100
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 3:
		monster = "Rogue"
		monster_health = 275
		monster_attack = 120
		monster_shield = 120
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 4:
		monster = "Rogue"
		monster_health = 300
		monster_attack = 145
		monster_shield = 145
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 5:
		monster = "Rogue"
		monster_health = 325
		monster_attack = 175
		monster_shield = 175
		return monster, monster_health, monster_attack, monster_shield
	elif func == "win" and level == 0:
		prize("potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. Sorry, it really was a lot of gold.""")
		experience(40)
	elif func == "win" and level == 1:
		prize("potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. As it turns out it was a huge amount of gold.""")
		experience(45)
	elif func == "win" and level == 2:
		prize("potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. At this point you could've just bought out the bad guys. 
Too bad.""")
		experience(50)
	elif func == "win" and level == 3:
		prize("big potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. This is kind of rediculous.""")
		experience(60)
	elif func == "win" and level == 4:
		prize("big potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. Maybe you should call the programmer and see what you can do about this, you deserve all this gold.""")
		experience(70)
	elif func == "win" and level == 5:
		prize("big potion")
		prize("""
Should've been a huge bag of gold here, but the programmer never included gold in the whole scheme of things. Have you seen a mountain? Yes like the one you came through not too long ago. You couldv'e buried that mountain with this mountain of gold you've 
earned. Tis a shame.""")
		experience(80)
	else:
		print "Sorry I can't do that."

# Same as above, but for the major dragon battle at the bottom of the caverns
def dragon_battle(func):
	global monster, monster_health, monster_attack, monster_shield, level
	if func == "stats" and level == 0:
		monster = "Dragon"
		monster_health = 250
		monster_attack = 85
		monster_shield = 95
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 1:
		monster = "Dragon"
		monster_health = 300
		monster_attack = 95
		monster_shield = 105
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 2:
		monster = "Dragon"
		monster_health = 350
		monster_attack = 110
		monster_shield = 120
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 3:
		monster = "Dragon"
		monster_health = 400
		monster_attack = 130
		monster_shield = 150
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 4:
		monster = "Dragon"
		monster_health = 450
		monster_attack = 155
		monster_shield = 175
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 5:
		monster = "Dragon"
		monster_health = 500
		monster_attack = 185
		monster_shield = 205
		return monster, monster_health, monster_attack, monster_shield
	elif func == "win" and level == 0:
		experience(130)
		prize("Dragon Scale")
		prize("potion")
		prize("potion")
	elif func == "win" and level == 1:
		experience(140)
		prize("Dragon Scale")
		prize("potion")
		prize("potion")
		prize("potion")
	elif func == "win" and level == 2:
		experience(150)
		prize("Dragon Scale")
		prize("big potion")
		prize("big potion")
	elif func == "win" and level == 3:
		experience(160)
		prize("Dragon Scale")
		prize("big potion")
		prize("big potion")
	elif func == "win" and level == 4:
		experience(170)
		prize("Dragon Scale")
		prize("big potion")
		prize("big potion")
	elif func == "win" and level == 5:
		experience(180)
		prize("Dragon Scale")
		prize("big potion")
		prize("big potion")
		prize("big potion")

# Same as above but for the battle to gain the wolf races confidence
def wolf_battle(func):
	global monster, monster_health, monster_attack, monster_shield, level
	if func == "stats" and level == 0:
		monster = "Wolf"
		monster_health = 200
		monster_attack = 80
		monster_shield = 80
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 1:
		monster = "Wolf"
		monster_health = 250
		monster_attack = 90
		monster_shield = 90
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 2:
		monster = "Wolf"
		monster_health = 300
		monster_attack = 105
		monster_shield = 105
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 3:
		monster = "Wolf"
		monster_health = 350
		monster_attack = 125
		monster_shield = 125
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 4:
		monster = "Wolf"
		monster_health = 400
		monster_attack = 150
		monster_shield = 150
		return monster, monster_health, monster_attack, monster_shield
	elif func == "stats" and level == 5:
		monster = "Wolf"
		monster_health = 450
		monster_attack = 180
		monster_shield = 180
		return monster, monster_health, monster_attack, monster_shield
	elif func == "win" and level == 0:
		experience(90)
		prize("Wolf Fang")
		prize("potion")
	elif func == "win" and level == 1:
		experience(100)
		prize("Wolf Fang")
		prize("potion")
		prize("potion")
	elif func == "win" and level == 2:
		experience(110)
		prize("Wolf Fang")
		prize("big potion")
	elif func == "win" and level == 3:
		experience(120)
		prize("Wolf Fang")
		prize("big potion")
	elif func == "win" and level == 4:
		experience(130)
		prize("Wolf Fang")
		prize("big potion")
	elif func == "win" and level == 5:
		experience(140)
		prize("Wolf Fang")
		prize("big potion")
		prize("big potion")

# Randomly picks one of the monsters above when called during a travel block. Uses a global list like a stack to check what the last battle was to prevent repeat troll/rogue battles.  Not sure if it works. It works.
def random_battle_decider():
	global monster
	battle = random.randint(0,100)
	last_monster = monster_list.pop()
	monster_list.append(last_monster)
	if battle in range(0,44):
		random_enemy_one("stats")
		monster_list.append("Goblin")
	elif battle in range(45,65) and last_monster != "Troll":
		random_enemy_two("stats")
		monster_list.append("Troll")
	elif battle in range(45,65) and last_monster == "Troll":
		random_battle_decider()
	elif battle in range(66,100) and last_monster != "Rogue":
		random_enemy_three("stats")
		monster_list.append("Rogue")
	elif battle in range(66,100) and last_monster == "Rogue":
		random_battle_decider()

# Used to decide the damage done by monster attacks and my attacks during battles, still needs to be adjusted for difficulty 
def damage_engine():
	global attack, shield, monster_attack, monster_shield, monster_damage, player_damage
	if attack > 0 and shield > 0 and monster_attack > 0 and monster_shield > 0:
		monster_damage = ((random.randint(25,35) * monster_attack) / (shield * 2))
		player_damage = ((random.randint(25,40) * attack) / (monster_shield/2))
		return monster_damage, player_damage
	else:
		print "No monster loaded"

#takes passed variable for character stats and monster stats, plays out battles with healing etc.  
def battle_engine():
	global monster_damage, player_damage, health, monster_health, monster
	print_slowly("\n\t***")
	print_slowly("\nYou have found a %r in your travels!" % monster)
	battling = True
	while battling == True:
		damage_engine()
		print_slowly("\nThe %r attacks you and does %r damage!" % (monster, monster_damage))
		health = health - monster_damage
		print_slowly("\nYou have %r health left." % health)
		if health > 0 and monster_health > 0:
			print_slowly("\nYou can attack back or use something from your inventory.")
			attack = raw_input("\n> ")
			if "attack" in attack:
				print_slowly("\nYou strike back and do %r damage!" % player_damage)	
				monster_health = monster_health - player_damage
				print_slowly("\nThe %r has %r health left." % (monster, monster_health))
				if monster_health <= 0:
					print_slowly("\nYou won! The %r fell to your sword." % monster)
					if monster == "Goblin":
						random_enemy_one("win")
						break
					elif monster == "Troll":
						random_enemy_two("win")
						break
					elif monster == "Rogue":
						random_enemy_three("win")
						break
					elif monster == "Wolf":
						wolf_battle("win")
						break
					elif monster == "Dragon":
						dragon_battle("win")
						break
					else:
						print "I don't think you were supposed to be fighting a %r" % monster
						battling = False
			elif "potion" in attack:
				heal("potion")
			elif "big" in attack:					
				heal("big potion")
			else:
				print_slowly("\nYou missed your chance trying to %r" % attack)
		else:
			print_slowly("\nYou were defeated by the mighty %r" % monster)
			dead("")

def plainsmen_puzzle():
	print_slowly("""
Wiseman: "Give me food, and I will live; Give me water and I will die. What am I?" """)
	answer_one = raw_input("\n\t> ")
	if "fire" in answer_one:
		print_slowly("""
Wiseman: "Correct!" """)
	else:
		print_slowly("""
Wiseman: "That is not correct. How can we trust a man who cannot solve a simple puzzle? Guards! Take him away!" """)
		dead("")
	print_slowly("""
Wiseman: "Next; What can run but never walks, has a mouth but never talks, has a head but never weeps, has a bed but never sleeps?"\n""")
	answer_two = raw_input("\t> ")
	if "river" in answer_two:
		print_slowly("""
Wiseman: "Correct!" """)
	else:
		print_slowly("""
Wiseman: "That is not correct. How can we trust a man who cannot solve a simple puzzle? Guards! Take him away!" """)
		dead("")
	print_slowly(""" 
Wiseman: "Next; Until I am measured, I am not known, but how you will miss me when I have flown! What am I?"\n""")
	answer_three = raw_input("\t> ")
	if "time" in answer_three:
			print_slowly("""
Wiseman: "Correct! I guess you can be trusted after all. We will give you our allegiance in battle.""")
			prize("Horse Shoe")
	else:
		print_slowly("""
Wiseman: "That is not correct. How can we trust a man who cannot solve a simple puzzle? Guards! Take him away!" """)
		dead("")

def dead(func):
	if func == "":
		print_slowly( """
Without you and the completion of your heroic quest the world will come to an end.
Good Job.""")
		sleep(1)
		if inventory.count("Tissues") > 0:
			print_slowly("\nDuring your time on this planet you collected %r Tissues!" % inventory.count("Tissues"))
		print_slowly("\nWould you like another chance to save your people?\n")
		do_it_again = raw_input("\n> ")
		if "yes" in do_it_again:
			char_stats("reset")
			main_story_line()
		else:
			print_slowly("\nHave a beautiful time!\n")
			exit()
	elif func == "end":
		sleep(1)
		if inventory.count("Tissues") > 0:
			print_slowly("\nDuring your time on this planet you collected %r Tissues!" % inventory.count("Tissues"))
		print_slowly("\nWould you like another chance to save your people?\n")
		do_it_again = raw_input("\n> ")
		if "yes" in do_it_again:
			char_stats("reset")
			main_story_line()
		else:
			print_slowly("\nHave a beautiful time!\n")
			exit()

# Prints text slowly with a random speed between 0.1 and 0.3 seconds to simulate typing! Cool!!
def print_slowly(text):
	for c in text:
		sys.stdout.write(c)
		sys.stdout.flush()
		seconds = "0.0" + str(randrange(6, 9, 6))
		seconds = float(seconds)
		sleep(seconds)
	
def main_story_line():
	char_stats("start")
	print_slowly( """
You walk over a hill and there are three paths in front of you. You sense a great evil in
the distance, what it is you do not know. Do you chose to venture forth and save your world? The path to the south leads to a dark forest, the path to the east leads to a great mountain, the path to the northeast leads to a vast plain.""")
	path_choice()

def path_choice():
	print_slowly("\nYou can go to the forest, the mountain, the plains, or to the far east.")
	print_slowly("\nWhich path do you choose?")
	choice = raw_input("\n> ")
	if "forest" in choice and inventory.count("Wolf Fang") == 0:
		forest_path()
	elif "forest" in choice and inventory.count("Wolf Fang") == 1:
		print_slowly("\nYou have already traveled that path, why not try a new one?")
		path_choice()
	elif "mountain" in choice and inventory.count("Dragon Scale") == 0:
		mountain_path()
	elif "mountain" in choice and inventory.count("Dragon Scale") == 1:
		print_slowly("\nYou have already traveled that path, why not try a new one?")
		path_choice()
	elif "plains" in choice and inventory.count("Horse Shoe") == 0:
		plains_path()
	elif "plains" in choice and inventory.count("Horse Shoe") == 1:
		print_slowly("\nYou have already traveled that path, why not try a new one?")
		path_choice()
	elif "east" in choice:
		great_battle()
	else:
		print_slowly("\nYou must choose a path")
		path_choice()
		
def forest_path():
	print_slowly("\nYou head towards the forest, it is only a days travel away.")
	random_battle_decider()
	battle_engine()
	print_slowly("\nYou take up camp at the entrance the to forest.")
	heal("sleep")
	print_slowly( """
The next day you head into the forest. It is overgrown and very dark once you are underneath the canopy. The mountain is visible off in the distance.""")
	random_battle_decider()
	battle_engine()
	print_slowly("\nYou find a old dead oak tree to set up camp in.")
	heal("sleep")
	print_slowly( """
You are awoken in the early hours of the morning by the muffled sound of steps.  They are light on the ground and it seems as though there are several of them.  The steps stop and you hear a sniffing sound. You draw your sword a leap from the hole in tree!
	
There is no one there. 
You look around for a trail to follow but there is none. Unable to rest again you head deeper into the forest. Around midday you find your first sign, a small bit of fur next to a pine tree. It is grey and white.....
Wolves. You continue on.""")
	random_battle_decider()
	battle_engine()
	print_slowly("\nAfter a long day you take up camp near a small stream.")
	heal("sleep")
	print_slowly( """
You wake up to a bit of sunshine poking through the trees. It is refreshing to see some light in all this darkness. You wash up in the stream and make your first hot breakfast in days. Three sunny side up eggs, bacon, thick toast and coffee. Mmmmmm.
Anyways there are some Wolf prints in the mud across the stream from you. You follow them for most of the day until they peter out to nothing.""")
	random_battle_decider()
	battle_engine()
	print_slowly( """
You push forward looking for more signs until darkness falls, time to set up camp.""")
	heal("sleep")
	print_slowly( """
When you pack up in the early morning it is a dark and misty day. You can hardly see 15 feet in front of you. You carefully trek forward following a straight line through the forest.""")
	random_battle_decider()
	battle_engine()
	print_slowly( """
After several more hours of travel you come upon a dark figure in the mist. As you slowly approach you see what appears to be a statue. It is a huge Wolf standing over a fallen Wolf. You wonder where it came from and what it signifies.""")
	random_battle_decider()
	battle_engine()
	print_slowly( "\nYou set up camp just outside the view of the statue.")
	heal("sleep")
	print_slowly( """
When you wake there are foot prints everywhere. They found you in the night, but left you alone? You pack your things and follow their foot steps. A few hours in the Wolves ambush you! You pull your sword but it is no use, you are surrounded.""")
	print_slowly( """
Wolf: "Why are you following us human!"
You: "I seek your allegance against the great evil that grows in the Far East!"
Wolf: "You want us to side with you! You who hunts us down and wears our hides to taunt us!"
You: "We must put our differences aside and fight together, there is an army gathering, an army like no other that seeks to wipe us all out! I urge you to come with me and fight together, and we can settle our own differences later."
Wolf: "We have seen the armies gathering. We will not travel with you, but we will meet you on the battle field to save our home, only on one condition. You will prove your strength and conviction by defeating one of our soldiers in a fight to the death!."
You: "Very well." """)
	wolf_battle("stats")
	battle_engine()
	print_slowly( """
After gaining the trust of the Wolves you head north out of the forest and camp on its edge.""")
	heal("sleep")
	print_slowly( """
You awake and see two paths in front of you. To the north is the great mountain, beyond that are the great plains, to the east on the horizon you can see a great fire burning where the armies gather to fight you.""")
	path_choice()
	
def mountain_path():
	print_slowly("""
You walk towards the mountain. It is a great distance away, yet it already looms over the land. The land here is barren and dry. As you walk you feel a presence behind you....""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
You spend the rest of your day moving ever closer towards the mountain. You find a patch of brush to rest in.""")
	heal("sleep")
	print_slowly("""
The sun is bright today and beats down on you. Travel is hard and slow in the heat. You take a break at an abandoned hut on the side of the road. As you continue on the mountain gets ever larger. You will reach it by nightfall.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
The sun falls to the horizon yet again as you set up camp at the base of the mountain.""")
	heal("sleep")
	print_slowly("""
The next day you start your trek up the mountain. There is barely a discernible path and it is steep and treacherous. As you climb higher and higher the air gets thinner. There seems to be no end in sight.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
You finally reach a plateau that is suitable for a camp site. The sunset at this height is astounding. You can see for miles!""")
	heal("sleep")
	print_slowly("""
Before midday you find an opening in the great mountain. On either side of the doorway is a great Goblin statue covered in gold trinkets and giant weapons. Maybe this wasn't such a great idea! You move forward and into the great mountain. With very little light to see with time seems to stand still.""")
	sleep(1)
	print_slowly("""
You feel as though you are traveling down the path for hours. At last you reach a great door, it is sitting ajar. You enter and find a huge city carved into the interior of the mountain. It appears to be completely deserted. Hoping to find a way through the mountain you travel down and into the city.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
The path is often unclear and winding. There are great halls and small rooms where the inhabitants once lived. The city is cleverly lit with sunbeams reflected around the different rooms. You find very little sign of the Goblins, as though they all packed up and left one day. After several hours you set up camp in a small banquet hall.""")
	heal("sleep")
	print_slowly("""
You awake in the morning having overslept many hours. The city is quiet and peaceful. As you reach the center of the city there are huge fires along your path to light the way. It would appear your not the only one here. Your path leads to a huge building in the city center, what appears to be the main hall. As you enter you are surprised to find a great Dragon! It's no wonder all the Goblins up and left. Before you can blink the Dragon sees you and slams the door shut with its spiked tail. 
Dragon: What brings you here little man?"
You: "I came in search of the Goblin folk to seek their aid in war!"
Dragon: "As you can see they are all gone, this is my city now!"
You: "Not for long my friend, a great evil is gathering power in the far East, if we do not fight together it will consume all of the land.
Dragon: "No one would dare challenge to take this mountain from me! I will confront them if they come and devour them all!"
You: "This enemy is too great even for you. As we speak they gather thousands to conquer us. The only way is if we strike as one! My people could use your help, come, fight with us!!."
Dragon: "I care not for your peoples troubles, but I do appreciate a good war. I will fight with you, but first must prove your strength to me in battle!" """)
	dragon_battle("stats")
	battle_engine()
	print_slowly("""
Dragon: "You have proven yourself to be a worthy ally, I hope for your sake that the rest of your people show your skill. Here open this chest and take what armor you will, that Bronze armor will get you nowhere when the great battle is at hand.""")
	weapon_armor_choice()
	print_slowly("\nYou rest in the great hall.")
	heal("sleep")
	print_slowly("""
The Dragon shows you the way out of the city and promises to meet you on the battle field. You look out and see the great plains to the north of you. There is a great fire burning in the east. Your people told rumors of a great kiln that the enemy burns to forge weapons for its armies. A kiln big enough to throw entire trees into. To the south there is a dark forest.""")
	path_choice()
	
def plains_path():
	print_slowly("""
You make your way to the plains in the north. Here there are vast rolling hills as far as you can see. In one of these great valleys the plainsmen live, you seek their allegiance in the great war ahead.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
You are wary of sleeping out in the open but there is no cover here. You do your best to set up camp in the shadow of a hill.""")
	heal("sleep")
	print_slowly("""
The next day you eye a herd of horses of the distance, heading north east. You follow them in hopes that they lead you to their people. The plainsmen raise and sell all of the horses in the land. """)
	random_battle_decider()
	battle_engine()
	print_slowly("""
The horses are still far ahead of you but their tracks are easy to follow. You camp in another small valley""")
	heal("sleep")
	print_slowly("""
You awake to find the herd has slowed and slept only in the next valley over. You manage to rope a young mustang to ease your weary feet. The herd continues on bringing you closer to the plainsmen.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
As the sun sets the herd slows and stops to rest by a small stream. You let the mustang free and set up camp a few paces up the stream from the pack.""")
	heal("sleep")
	print_slowly("""
As you pack your things the next morning you see flags off in the distance. At last you have found their city. It is a large camp with many knights. When you get close enough there are two guards sent out to meet you. 
Guard: "What brings you all this way?"
You: "I come to seek your allegiance in the coming war. There is a great evil gathering in the east, if we are to be free we must fight together!"
Guard: "We are aware of the evil that gathers. They have stolen many of our horses the night. We may not have seen eye to eye in the past but that no longer matters in this time of need. Come, you must be tested if we are to trust you."
The guards lead you to their encampment. There they bring you to a small hut covered in runes. Once inside you meet a wise man. 
Wiseman: "I will ask you three questions to test your judgement and your honesty. Answer incorrectly and you will see this world no more.""")
	plainsmen_puzzle()
	print_slowly("""
The plainsmen lead you to the southeastern edge of their land and promise to meet you on the battle field. There is a mountain to the south and a dark forest beyond that. To the east the enemy is gathering to fight you.""")
	path_choice()

def great_battle():
	print_slowly("""
You travel east towards to great fires in the distance. The castle they have built to protect themselves is a few days off in the distance. As you get closer the land becomes more and more barren. You can see great tracks where they have come to strip the land to fuel their great forges.""")
	random_battle_decider()
	battle_engine()
	print_slowly("""
You come upon an abandoned town, all of the inhabitants taken for work slaves or forced to fight for the enemy. You shudder to think that this is what will happen to your hometown if you are not successful. You find a suitable place to rest. You do not sleep very well.""")
	heal("sleep")
	print_slowly("""
The next morning you wake to the sound of footsteps. They found you already! As you peer outside you see a little old man shuffling towards the well in the center of the town. Good thing you looked before striking!
You: "Old man what happened here?"
Old Man: "The enemy came and took all of people of course. They left me behind to die proclaiming my uselessness."
You: "Tell me what did they look like?"
Old Man: "A great mix of creatures. Goblins, Trolls, and Men. They destroyed everything they touched. Young man, why do you ask such questions?"
You: "I have come ahead of my people to destroy this great evil and save our land. I have traveled far to unite the warring states of this land."
Old Man: "You bear a heavy task, come to my home and let me show you something."
The old man brings you across town to a humble home. Inside there is a small fire burning next to an anvil and many forging tools. 
Old Man: "I hid these things from them just in case. I used to be renowned smith back in my day. Let me see those weapons you carry and perhaps we can make them a bit stronger." """)
	weapon_armor_enhance()
	print_slowly("""
Old Man: "That is the best I could do. I hope that it helps you when you need it."
You: "I cannot thank you enough, I will not forgot what you have done for me."
You leave the town and travel the last few miles to the evil castle. Just behind you a dust cloud floats in the sky. Your people and their armies have come to meet you at the gates." """)
	if inventory.count("Horse Shoe") == 1 and inventory.count("Dragon Scale") == 1 and inventory.count("Wolf Fang") == 1:
		print_slowly("""
As you lead your armies into the gates of the castle you are met by the enemy. They outnumber you ten to one but your people fight with courage in their hearts and the love of their home on their minds. You make the enemy feel your pain and just as they regather to attack you from all sides the plainsmen appear from the north and join you! The ground starts shaking and you look up to see thousands of armored Wolves attacking from the south! You are distracted and caught off guard by an enemy soldier and he knocks you to the ground. As he reaches back to strike he is lifted into the air by the Dragon of the mountain and tossed away! With all of the nations in the land united the enemy is crushed! 

Victory!!

With the enemy defeated and the land free you have helped to bring in a new era of cooperation between the different people of your land. 

Good job!""")
		credits()
	if inventory.count("Horse Shoe") == 0 or inventory.count("Dragon Scale") == 0 or inventory.count("Wolf Fang") == 0:
		print_slowly("""
As you lead your armies into the gates of the castle you are met by the enemy. They outnumber you ten to one but your people fight with courage in their hearts and the love of their home on their minds. You make the enemy feel your pain and for a moment it appears as though you might win! But the enemy is too great in number and they come at you from all sides. Without the support of every free being in the land the war is lost. You have failed. Within days the enemy ventures forth and conquers every corner of the land.""")
		dead("end")

def credits():
	print_slowly("""\n\n
Thanks for playing my game, I hope you liked it! If you have comments, questions, bugs or if you want to help me make another game (I clearly need the help of a writer) feel free to contact me at healthynate@gmail.com or on twitter @natemallison.

Have a beautiful time!

~Nathan Mallison\n""")
	if inventory.count("Tissue") > 0:
		print_slowly("\n\nYou collected %r Tissues!" % inventory.count("Tissue"))
	
	
# expand ending

# make upper level enemies stronger, lower level goblins a bit stronger, wolf and dragon battles stronger

# seems a touch boring, needs more in battle options and explorability! (Thats not a word)

# Things to add: more battle options, blocking and dodging. Instead of forcing sleep let the player decide when to move on, give options to go back, sleep, check stats, go forward. This one will require re-writing the text. 

# Figure out how to prevent keyboard input during print_slowly function execution

# convert to OOP: character class (stat creation and reset functions, experience function, weapon upgrade functions, prize function, healing function), enemy class (enemy stat loader function), game class (main story line, death function, print_slowly function, main path text, credits, path choice), battle class (random battle decider, battle engine, damage engine).


# gets things going!!
main_story_line()