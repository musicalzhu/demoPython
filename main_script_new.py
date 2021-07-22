import pvrhino
import struct
import pyaudio
import os
from termcolor import colored
from os import path
import chess
import chess.svg
import time
import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5 import QtCore
import serial

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), 'microphone-results.wav' )
GAME_IN_PROGRESS=False
BOARD_OFFCET_TO_GRAVEYARD = 25 #ON X most far point +20mm
HALF_CELL_DISTANCE = 0 #WILL be changed down
GRAVEYARD_X_COORDINATE = 0 #WILL be changed down



board = chess.Board()


coordinates_dictionary_A = {'A1': ['x',0,'y',0],'A2': ['x',0,'y',0],'A3': ['x',0,'y',0],'A4': ['x',0,'y',0],'A5': ['x',0,'y',0],'A6': ['x',0,'y',0],'A7': ['x',0,'y',0],'A8': ['x',0,'y',0]}
coordinates_dictionary_B = {'B1': ['x',0,'y',0],'B2': ['x',0,'y',0],'B3': ['x',0,'y',0],'B4': ['x',0,'y',0],'B5': ['x',0,'y',0],'B6': ['x',0,'y',0],'B7': ['x',0,'y',0],'B8': ['x',0,'y',0]}
coordinates_dictionary_C = {'C1': ['x',0,'y',0],'C2': ['x',0,'y',0],'C3': ['x',0,'y',0],'C4': ['x',0,'y',0],'C5': ['x',0,'y',0],'C6': ['x',0,'y',0],'C7': ['x',0,'y',0],'C8': ['x',0,'y',0]}
coordinates_dictionary_D = {'D1': ['x',0,'y',0],'D2': ['x',0,'y',0],'D3': ['x',0,'y',0],'D4': ['x',0,'y',0],'D5': ['x',0,'y',0],'D6': ['x',0,'y',0],'D7': ['x',0,'y',0],'D8': ['x',0,'y',0]}
coordinates_dictionary_E = {'E1': ['x',0,'y',0],'E2': ['x',0,'y',0],'E3': ['x',0,'y',0],'E4': ['x',0,'y',0],'E5': ['x',0,'y',0],'E6': ['x',0,'y',0],'E7': ['x',0,'y',0],'E8': ['x',0,'y',0]}
coordinates_dictionary_F = {'F1': ['x',0,'y',0],'F2': ['x',0,'y',0],'F3': ['x',0,'y',0],'F4': ['x',0,'y',0],'F5': ['x',0,'y',0],'F6': ['x',0,'y',0],'F7': ['x',0,'y',0],'F8': ['x',0,'y',0]}
coordinates_dictionary_G = {'G1': ['x',0,'y',0],'G2': ['x',0,'y',0],'G3': ['x',0,'y',0],'G4': ['x',0,'y',0],'G5': ['x',0,'y',0],'G6': ['x',0,'y',0],'G7': ['x',0,'y',0],'G8': ['x',0,'y',0]}
coordinates_dictionary_H = {'H1': ['x',0,'y',0],'H2': ['x',0,'y',0],'H3': ['x',0,'y',0],'H4': ['x',0,'y',0],'H5': ['x',0,'y',0],'H6': ['x',0,'y',0],'H7': ['x',0,'y',0],'H8': ['x',0,'y',0]}
coordinates_dictionary =  {**coordinates_dictionary_A, **coordinates_dictionary_B,**coordinates_dictionary_C,**coordinates_dictionary_D,**coordinates_dictionary_E,**coordinates_dictionary_F,**coordinates_dictionary_G,**coordinates_dictionary_H}


board_picture = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="300" height="300" viewBox="0 0 300 300" id="smile" version="1.1">
        <path
            style="fill:#ffaaaa"
            d="M 150,0 A 150,150 0 0 0 0,150 150,150 0 0 0 150,300 150,150 0 0 0 
                300,150 150,150 0 0 0 150,0 Z M 72,65 A 21,29.5 0 0 1 93,94.33 
                21,29.5 0 0 1 72,124 21,29.5 0 0 1 51,94.33 21,29.5 0 0 1 72,65 Z 
                m 156,0 a 21,29.5 0 0 1 21,29.5 21,29.5 0 0 1 -21,29.5 21,29.5 0 0 1 
                -21,-29.5 21,29.5 0 0 1 21,-29.5 z m -158.75,89.5 161.5,0 c 0,44.67 
                -36.125,80.75 -80.75,80.75 -44.67,0 -80.75,-36.125 -80.75,-80.75 z"
        />
    </svg>
    """
_serial = serial.Serial()

def connect_to_Arduino():
    _serial.baudrate = 115200
    # Open grbl serial port
    try:
        _serial.port = '/dev/ttyACM0'
        _serial.open()
        _serial.write(str.encode("\r\n\r\n")) # Wake up grbl

    except serial.SerialException:
        try:
            _serial.port = '/dev/ttyACM1'
            _serial.open()
            _serial.write(str.encode("\r\n\r\n")) # Wake up grbl
        except serial.SerialException:
            try:
                _serial.port = '/dev/ttyACM2'
                _serial.open()
                _serial.write(str.encode("\r\n\r\n")) # Wake up grbl
            except serial.SerialException:
                    try:
                        _serial.port = '/dev/ttyUSB0'
                        _serial.open()
                        _serial.write(str.encode("\r\n\r\n")) # Wake up grbl
                    except serial.SerialException:
                        print ("There is no GRBL controller conneted")


def reconnect_Arduino():
    if (_serial.is_open):
        _serial.close()
    connect_to_Arduino()

def init_board_window():
    def reload_svg():
        
        svg_bytes = bytearray(board_picture, encoding='utf-8')
        svgWidget.renderer().load(svg_bytes)
        svgWidget.update()   

    svg_bytes = bytearray(board_picture, encoding='utf-8')
    app = QApplication(sys.argv)
    svgWidget = QSvgWidget()
    svgWidget.renderer().load(svg_bytes)
    svgWidget.setGeometry(200,5,440,440)
    svgWidget.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda : reload_svg())
    timer.start(500)
    sys.exit(app.exec_())

    #QtWidgets.QApplication.instance().exec_()




def start_new_game():
    global GAME_IN_PROGRESS
    global board_picture
    board.reset_board()
    board_picture = chess.svg.board(board)
    GAME_IN_PROGRESS=True
    #write_to_grbl('$?')
    write_to_grbl('$21=0')#disable hard limits
    write_to_grbl('$23=3')#set homing corner
    write_to_grbl('$24=100')#speed fall back after homing switch
    write_to_grbl('$27=3')#go 3 mm away from home after homing
    write_to_grbl('$26=500')#debounce msec after homing switch
    ##write_to_grbl('G50 G21')
    write_to_grbl('$X')
    write_to_grbl('F5000')
    write_to_grbl('$H')#go home
    #make_a_move_in_hardware('H8','H8')
    #write_to_grbl('G1 y0 x0 F5000')
    
    
    
    

def fillup_the_coordinates_dictionary():
    global coordinates_dictionary
    global HALF_CELL_DISTANCE
    global GRAVEYARD_X_COORDINATE
    
    A1_x_offset = 35 #A1 is 20mm away from X home postion
    A1_y_offset = 12
    from_A1_to_A8_distance = 222 #how many mm is the board on y direction
    from_A1_to_H1_distance = 222
    y_between_cell_distance = 32#int(from_A1_to_A8_distance/8) #should be integer, not float
    x_between_cell_distance = 32#int(from_A1_to_H1_distance/8)
    HALF_CELL_DISTANCE = int((x_between_cell_distance+y_between_cell_distance)/4)
    GRAVEYARD_X_COORDINATE = A1_x_offset+from_A1_to_H1_distance+BOARD_OFFCET_TO_GRAVEYARD

    
    x = A1_x_offset
    y = A1_y_offset
    count = 1
    while count <= 8:
        coordinates_dictionary['A'+str(count)][1]=x 
        coordinates_dictionary['A'+str(count)][3]=y
        coordinates_dictionary['B'+str(count)][1]=x+(x_between_cell_distance*1)
        coordinates_dictionary['B'+str(count)][3]=y
        coordinates_dictionary['C'+str(count)][1]=x+(x_between_cell_distance*2)
        coordinates_dictionary['C'+str(count)][3]=y
        coordinates_dictionary['D'+str(count)][1]=x+(x_between_cell_distance*3)
        coordinates_dictionary['D'+str(count)][3]=y
        coordinates_dictionary['E'+str(count)][1]=x+(x_between_cell_distance*4)
        coordinates_dictionary['E'+str(count)][3]=y
        coordinates_dictionary['F'+str(count)][1]=x+(x_between_cell_distance*5)
        coordinates_dictionary['F'+str(count)][3]=y
        coordinates_dictionary['G'+str(count)][1]=x+(x_between_cell_distance*6)
        coordinates_dictionary['G'+str(count)][3]=y
        coordinates_dictionary['H'+str(count)][1]=x+(x_between_cell_distance*7)
        coordinates_dictionary['H'+str(count)][3]=y

        y = y+y_between_cell_distance
        count += 1
    

def listen_then_recognize():
    pa = None
    handle = None
    audio_stream = None

    try:
        pa = pyaudio.PyAudio()
        inpath = "/home/pi/python/picovoice/chess_en_raspberry-pi_2021-08-02-utc_v1_6_0.rhn"

        handle = pvrhino.create(inpath)

        audio_stream = pa.open(
                            rate=handle.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=handle.frame_length)

        def get_next_audio_frame():
            pcm = audio_stream.read(handle.frame_length)
            pcm = struct.unpack_from("h" * handle.frame_length, pcm)
            return pcm

        while True:
            is_finalized = handle.process(get_next_audio_frame())

            if is_finalized:
                inference = handle.get_inference()
                if not inference.is_understood:
                    # add code to handle unsupported commands
                    print("unsupported commands!")
                else:
                    intent = inference.intent
                    slots = inference.slots
                    # add code to take action based on inferred intent and slot values
                    print("intent: " + str(intent) + "  slots: " + str(slots))
                    return slots
    
    finally:
        if handle is not None:
            handle.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()

def check_move(source,destination):
    try: 
        move = chess.Move.from_uci(source.lower()+destination.lower())
        if (move in board.legal_moves):
            return True
        else:
            return False
    except ValueError:
         return False
        
        
        
def write_to_grbl (string_of_grbl_code):
    _serial.flushInput()  # Flush startup text in serial input
    for x in range(3):
        _serial.write(str.encode(string_of_grbl_code + '\n')) # Send g-code block to grbl
        print ('GRBL Sent: '+string_of_grbl_code)
        grbl_out = _serial.readline().decode('utf-8') # Wait for grbl response with carriage return
        print ('GRBL Received: '+grbl_out)
        if (grbl_out.strip() == 'ok'):
            break
    else:
        print ("Sending to grbl controller failed 3 times, trying reconnect serial port")       
        for x in range(3):
            reconnect_Arduino()
            _serial.write(str.encode(string_of_grbl_code + '\n')) # Send g-code block to grbl
            print ('GRBL Sent: '+string_of_grbl_code)
            grbl_out = _serial.readline().decode('utf-8') # Wait for grbl response with carriage return
            print ('GRBL Received: '+grbl_out)
            if (grbl_out.strip() == 'ok'):
                break
            print ("Reset GRBL controller!")
            time.sleep(1)
        else:
            print ("Too many fails. Move skipped")
    
    
def make_a_move_in_hardware(source,destination):
    #first need to check is the destination of chess piece ocupuied, if yes first clean destination cell

    destination_letter = list(destination.lower())[0]
    destination_number = list(destination)[1]
    dest_cell_index = chess.square(chess.FILE_NAMES.index(destination_letter),chess.RANK_NAMES.index(destination_number))
    
    source_coordinate_x = coordinates_dictionary[source][1]
    source_coordinate_y = coordinates_dictionary[source][3]
        
    destination_coordinate_x = coordinates_dictionary[destination][1]
    destination_coordinate_y = coordinates_dictionary[destination][3]
    print (source_coordinate_x, source_coordinate_y,'  ', destination_coordinate_x, destination_coordinate_y)
    write_to_grbl('F5000') #setup grbl feed rate (speed of move)
    
    if (board.piece_at(dest_cell_index) != None): #cell is not empty
        write_to_grbl('G1 '+'x'+str(destination_coordinate_x)+'y'+str(destination_coordinate_y)) #go to cell first
        write_to_grbl('M07')#turn on magnet
        write_to_grbl('G1 '+'y'+str(destination_coordinate_y+HALF_CELL_DISTANCE))# minimove to the border between cels
        write_to_grbl('G1 '+'x'+str(GRAVEYARD_X_COORDINATE)) #drug piece to th graveyard
        write_to_grbl('M09')#turn off magnet
     
    
    #now move the piece from source to destination
    write_to_grbl('G1 '+'x'+str(source_coordinate_x)+' y'+str(source_coordinate_y)) #go to cell first
    #print ('G1 '+'x'+str(source_coordinate_x)+' y'+str(source_coordinate_y))
   
    write_to_grbl('M07')#turn on magnet
    #below are different strategies depending on what direction is the destination
    if (source_coordinate_x == destination_coordinate_x):
        if (source_coordinate_y < destination_coordinate_y): #go up sraight
            write_to_grbl('G1 '+'x'+str(source_coordinate_x+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go up between cels
            
        if (source_coordinate_y > destination_coordinate_y): #go down sraight
            write_to_grbl('G1 '+'x'+str(source_coordinate_x+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go down between cels
    if (source_coordinate_x < destination_coordinate_x):
        
        if (source_coordinate_y == destination_coordinate_y): #go right straight
            write_to_grbl('G1 '+'y'+str(source_coordinate_y+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x))#go right between cels
            
        if (source_coordinate_y < destination_coordinate_y): #go up right
            write_to_grbl('G1 '+'y'+str(source_coordinate_y+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x+HALF_CELL_DISTANCE))#go right between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go up between cels
            
        if (source_coordinate_y > destination_coordinate_y): #go down righ
            write_to_grbl('G1 '+'y'+str(source_coordinate_y-HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x+HALF_CELL_DISTANCE))#go right between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go down between cels
    if (source_coordinate_x > destination_coordinate_x):
        
        if (source_coordinate_y == destination_coordinate_y): #go left straight
            write_to_grbl('G1 '+'y'+str(source_coordinate_y+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x))#go left between cels
            
        if (source_coordinate_y < destination_coordinate_y): #go up left
            write_to_grbl('G1 '+'y'+str(source_coordinate_y+HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x-HALF_CELL_DISTANCE))#go right between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go up between cels
            
        if (source_coordinate_y > destination_coordinate_y): #go down left
            write_to_grbl('G1 '+'y'+str(source_coordinate_y-HALF_CELL_DISTANCE))# minimove to the border between cels
            write_to_grbl('G1 '+'x'+str(destination_coordinate_x-HALF_CELL_DISTANCE))#go left between cels
            write_to_grbl('G1 '+'y'+str(destination_coordinate_y))#go down between cels
            
    write_to_grbl('G1 '+'x'+str(destination_coordinate_x)+' y'+str(destination_coordinate_y)) #make a final minimove to the destination
    write_to_grbl('M09')#turn off magnet

    
    
    
    
def make_a_move_in_software(source,destination):
    global board_picture
    print (source,"=>",destination)
    #print (coordinates_dictionary[source])
    #print (coordinates_dictionary[destination])
    source_letter = list(source.lower())[0] #example: A1 become a
    source_number = list(source)[1]#example:A1 become  1
    source_cell_index = chess.square(chess.FILE_NAMES.index(source_letter),chess.RANK_NAMES.index(source_number))#example: A1 is cell index = 0 (out of 63)
    
    destination_letter = list(destination.lower())[0]
    destination_number = list(destination)[1]
    dest_cell_index = chess.square(chess.FILE_NAMES.index(destination_letter),chess.RANK_NAMES.index(destination_number))
    
    try:       
        board_picture = chess.svg.board(board,arrows =[(source_cell_index,dest_cell_index)]) #show arrow representing current move
        make_a_move_in_hardware(source,destination)
        board.push_uci(source.lower()+destination.lower())
        board_picture = chess.svg.board(board)#show chess board after the move
    except ValueError:
               print("move is invalid or illegal in the current position")

def check_game_status():
    if board.is_check() :
        print ("Check!")
    if board.is_checkmate() :
        print ("Check and mate!")
    if board.has_insufficient_material(chess.WHITE):
        print ("White doesn't have enough moves or chess pieces to win")
    if board.has_insufficient_material(chess.BLACK):
        print ("Black doesn't have enough moves or chess pieces to win")
    if board.is_game_over() :
        print ("Game is over with result:", board.result)
               
            
letterDic = {
"ALPHA": 'A',
"BRAVO": 'B',
"CHARLIE": 'C',
"DELTA": 'D',
"ECHO":'E',
"FOXTROT": 'F',
"GOLF": 'G',
"HOTEL": 'H'
}

numberDic = {
"ONE": 1,
"TWO": 2,
"THREE": 3,
"FOUR": 4,
"FIVE": 5,
"SIX": 6,
"SEVEN": 7,
"EIGHT": 8
}

def format_speech(recognized_text):

    from_letter = recognized_text.get("r1")
    from_number = recognized_text.get("l1")
    to_letter = recognized_text.get("r2")
    to_number = recognized_text.get("l2")
        
    from_letter = letterDic.get(from_letter.upper())
    from_number = numberDic.get(from_number.upper())
    to_letter = letterDic.get(to_letter.upper())
    to_number = numberDic.get(to_number.upper())
        
    return from_letter,from_number,to_letter,to_number



try:
    connect_to_Arduino()
    threading.Thread(target=init_board_window).start() #start a window where chess board will be shown in separate thread
    fillup_the_coordinates_dictionary()
    
    while True:
        if GAME_IN_PROGRESS:
            try:
                
                recognized_text = listen_then_recognize()
                print("Sphinx thinks you said:")
                print(colored (recognized_text, 'red'))
                from_letter,from_number,to_letter,to_number = format_speech(recognized_text)
                print("format_speech: " + from_letter + str(from_number) + to_letter + str(to_number))
                if (check_move(from_letter + str(from_number), to_letter + str(to_number)) == True):
                    make_a_move_in_software(from_letter + str(from_number), to_letter + str(to_number))
                    check_game_status()
                else:
                    print ("This move is not valid, try again")
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
                
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))
        else:
            start_new_game()
except KeyboardInterrupt:
    print("Ctrl-C was pressed, program terminated")
    if (_serial.is_open):
        _serial.close()