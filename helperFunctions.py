import discord, time, os, load, traceback, sys

def overAge18(dateOfBirth):
    today_year, today_month, today_day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
    dateOfBirth = dateOfBirth.split("/")
    user_year, user_month, user_day = int(dateOfBirth[2]), int(dateOfBirth[1]), int(dateOfBirth[0])
    age = today_year - user_year - ((today_month, today_day) < (user_month, user_day))
    return age >= 18
