import sys, time
import sevseg  # Импорт программы sevseg.py.
import psutil as si  # sYSTEMiNFO


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


try:
    battery = si.sensors_battery()
    print(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
    while battery.percent > 10:  # оставшийся заряд батареи в процентах.
        # Очищаем экран, выводя несколько символов новой строки:
        print('\n' * 2)

        secondsLeft = battery.secsleft  # приблизительное количество секунд, оставшихся до полной разрядки батареи.
        # Берем часы/минуты/секунды из secondsLeft:
        # Например: 7265 равно 2 часам 1 минуте 5 секундам.
        # 7265 // 3600 равно 2 часам:
        hours = str(secondsLeft // 3600)
        #  7265 % 3600 равно 65, и 65 // 60 равно 1 минуте:
        minutes = str((secondsLeft % 3600) // 60)
        #  А 7265 % 60 равно 5 секундам:
        seconds = str(secondsLeft % 60)

        # Получаем из модуля sevseg строковые значения для цифр:
        pDigits = sevseg.get_seven_segment_string(battery.percent, 2)
        pTopRow, pMiddleRow, pBottomRow = pDigits.splitlines()

        hDigits = sevseg.get_seven_segment_string(hours, 2)
        hTopRow, hMiddleRow, hBottomRow = hDigits.splitlines()

        mDigits = sevseg.get_seven_segment_string(minutes, 2)
        mTopRow, mMiddleRow, mBottomRow = mDigits.splitlines()

        sDigits = sevseg.get_seven_segment_string(seconds, 2)
        sTopRow, sMiddleRow, sBottomRow = sDigits.splitlines()

        # Отображаем цифры:
        print(pTopRow + '    ' + hTopRow + '   ' + mTopRow + '   ' + sTopRow)
        print(pMiddleRow + ' %  ' + hMiddleRow + ' * ' + mMiddleRow + ' * ' + sMiddleRow)
        print(pBottomRow + ' %  ' + hBottomRow + ' * ' + mBottomRow + ' * ' + sBottomRow)

        if battery.percent < 12:
            print('!!!')

        print()
        print('Рівень заряду в відсотках, час роботи до повного розряду')
        print('Press Ctrl-C to quit.')

        time.sleep(30)  # Вставляем паузу на 30 секунд.
        battery = si.sensors_battery()
except KeyboardInterrupt:
    print('Battery info, by Al Sweigart al@inventwithpython.com @ psutil (Giampaolo Rodola)')
    sys.exit()  # Если нажато сочетание клавиш Ctrl+C — завершаем программу.
