from random import choice
from time import sleep

suits = ['spades', 'hearts', 'clubs', 'diamonds']
ranks = {	"2": 		2,
			"3":		3,
			"4":		4,
			"5":		5,
			"6":		6,
			"7":		7,
			"8":		8,
			"9":		9,
			"10":		10,
			"Jack":		10,
			"Queen":	10,
			"King":		10,
			"Ace":		11
		}
		
class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
	
	def text(self):
		return self.rank + " of " + self.suit
		
	def getval(self):
		return ranks[self.rank]
		
def call(cards):			#függvény ami kiválaszt egy random kártyát
	call = choice(cards)
	cards.remove(call)
	return call

game = True

cards = []
for suit in suits:			#itt töltjük föl a cards listát az összes kártyával
	for rank in ranks:
		cards.append(Card(suit, rank))
		
money = 1000 #$
		
print("WELCOME TO A GAME OF BLACKJACK\nYou have 1000$ to start with")

while game:
	print("Balance:", money, "$")
	bet = int(input("\nPlace your bet: ")) #tét
	
	if bet>money or bet<0:
		break
	
	money -= bet
	profit = 0
	
	playercards = []
	dealercards = []
	
	playercards.append(call(cards))	#kezdő lapok
	dealercards.append(call(cards))
	playercards.append(call(cards))
	dealercards.append(call(cards))
	
	playerval = playercards[0].getval() + playercards[1].getval()
	dealerval = dealercards[0].getval() + dealercards[1].getval()
	player = True
	dealer = False
	hits = 0
	
	print("\nDealer's hand:")
	print(dealercards[0].text())
	
	if dealerval == 21:			#megnézzük hogy van-e blackjack a kezdőlapoknál
		print(dealercards[1].text())
		print("Total value:", dealerval)
		if playerval != 21:
			print("Dealer has BLACKJACK! You lose")
		else:
			print("\nYour hand:")
			print(playercards[0].text())
			print(playercards[1].text())
			print("Total value:", playerval)
			print("\nIt's a tie")
			profit = bet
			
		player = False
	
	while player:				#játékos köre
		print("\nYour hand:")
		for card in playercards:
			print(card.text())
		print("Total value:", playerval,"\n")
		if playerval==21:
			print("You win!")
			profit = 2.5*bet
			player = False
		elif playerval>21:
			aces = False
			for card in playercards:
				if card.rank == "Ace":
					aces = True
			if aces:
				playerval -= 10
			else:
				print("BUST! Dealer wins")
				player = False
		else:
			if hits == 3:
				print("You win!")
				profit = 1.5*bet
				player = False
			nextmove = input("\nWhat do you want to do? (hit/stand)\n")
			if nextmove == "hit":
				new = call(cards)
				playercards.append(new)
				playerval += new.getval()
				hits += 1
			elif nextmove == "stand":
				player = False
				dealer = True
			else:
				game = False
	
	while dealer:				#osztó köre
		for i in range(hits):
			new = call(cards)
			dealercards.append(new)
			dealerval += new.getval()
		
		print("\nDealer's cards:")
		for card in dealercards:
			print(card.text())
			sleep(2)
		print("Total value:", dealerval)
		
		if dealerval>21:
			aces = False
			for card in dealercards:
				if card.rank == "Ace":
					aces = True
			if aces:
				dealerval -= 10
			else:
				print("Dealer's busted! You win!")
				profit = 2*bet
				dealer = False
		else:
			if dealerval > playerval:
				print("Dealer wins")
			elif dealerval == playerval:
				print("It's a tie")
				profit = bet
			else:
				print("You win!")
				profit = 2*bet
		break
	
	money += profit
	
	another = input("Do you want to play again? (yes/no)\n")
	if another=="no":
		print("Thank you for playing! Please come again.")
		game = False
	elif another == "yes":
		for card in playercards:		#visszarendezés
			cards.append(card)
		for card in dealercards:
			cards.append(card)
	else:
		game = False