# stringsfuns package

# Author :- Thorati Jai Satya Sai Phanindra

# This package consists of various functions or methods related to the strings 

# In order to install this package , just type "pip install stringsfuns"

# stringsfuns package consists of a total of 28 methods

# length(string) -> gives the length of the string

# uppercase(string) -> converts all characters of string to uppercase

# lowercase(string) -> converts all characters of string to lowercase

# title(string) -> let us consider string = "string method" ,then the output of this method will be "String Method"

# swapping_case(string) -> let us consider string = "sTRINg" ,then the output of this method will be "StrinG"

# starts(s,s1,pos) -> let us consider the s = "string" and s1="s" and pos=0 ,then the output of this method will be True ,here the starts       method checks whether the starting position of the s starts with s1 , if it starts with s1 it returns True or else it returns False , keep in mind that indexes in strings starts with 0

# spliting_lines(s) -> let us consider the s="Hello world.My name is Rfg" ,then the output of this method will be a list which is equal to ["Hello world" , "My name is Rfg"]

# counting_char(s,s1,start,end) -> let us consider the s="string" and s1="t" and start=0 and end=5 ,then the output of this method will be 1 ,here it counts the occurence of the s1 in s from start parameter value to end parameter value , keep in mind that indexes in strings starts with 0

# finding(s,s1,start,end) -> let us consider the s="string" and s1="t" and start=0 and end=5 ,then the output of this method will be 1 , here it gives us the position of the s1 in s by considering the string "s" from start parameter value to end parameter value , keep in mind that indexes in strings starts with 0

# comparison(s,s1) -> Here this method compares two strings s and s1 and return True if they both are equal or else False

# concatenate(s,s1) -> Here this method concatenates two strings s and s1

# copy(s) -> copies the string into another variable

# reverse(s) -> reverses the string s

# replace(s,s1,s2) -> let s="string" and s1="t" and s2="g" and this method replaces all s1 with s2 in s

# capitalizes(s) -> let s="string" , then the output of this method will be "String"

# multiply(s,n) -> Here this method multiplis the string n times

# isalphanumeric(s) -> Returns True if the string s is alphanumeric

# isalphabets(s) -> Returns True if all the string characters are alphabets

# isdigits(s) -> Returns True if all the string characters are digits

# isuppers(s) -> Returns True if all the string characters are in uppercase

# islowers(s) -> Returns True if all the string characters are in lowercase

# isspaces(s) -> Returns True if all the string characters are spaces

# palindrome(s) -> Returns True if the string s is a palindrome

# pangram(s) -> Returns True if the string s is a pangram

# anagram(s,s1) -> Returns True if the string s and s1 are anagrams with respect to each other

# alphaorder(s) -> Returns the string which is sorted from ascending to descending order according to alphabets

# char_to_ascii(s) -> Returns a list of ascii values of each character of the string s

# dec_to_char(s) -> Let us consider that you have given a list of ascii values to the method , then this method will convert all the ascii values into their respective characters and joins all the characters into a string and returns that string

# Example:-

# from stringsfuns import length
# s='string'
# a=length(s)
# print(a)

# Output:- 
# 6

# I hope that the package stringsfuns helps you a lot