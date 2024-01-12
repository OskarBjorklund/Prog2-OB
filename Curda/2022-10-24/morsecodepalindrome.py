morsecode = 		{ 'A':'.-', 'B':'-...',
					'C':'-.-.', 'D':'-..', 'E':'.',
					'F':'..-.', 'G':'--.', 'H':'....',
					'I':'..', 'J':'.---', 'K':'-.-',
					'L':'.-..', 'M':'--', 'N':'-.',
					'O':'---', 'P':'.--.', 'Q':'--.-',
					'R':'.-.', 'S':'...', 'T':'-',
					'U':'..-', 'V':'...-', 'W':'.--',
					'X':'-..-', 'Y':'-.--', 'Z':'--..',
					'1':'.----', '2':'..---', '3':'...--',
					'4':'....-', '5':'.....', '6':'-....',
					'7':'--...', '8':'---..', '9':'----.',
					'0':'-----', ', ':'', '.':'', '?':'', ' ':'', 
					'/':'', '':'', '(':'', ')':'', "'":''}

def encrypt(message):
	cipher = ''
	for letter in message:
		cipher += morsecode[letter]

	return cipher

def main():
	message = input()
	result = encrypt(message.upper())

	palindrome = True
	
	for i in range (int(len(result)/2)+1):
		if result[i] != result[-1-i]:
			palindrome = False
	
	if palindrome == True:
		print("1")
	else:
		print("0")

main()