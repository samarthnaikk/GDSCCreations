from fpdf import FPDF
import random

class PDF(FPDF):
    def add_transparent_image(self, path, x, y, h, charc, w):
        if charc.isnumeric() and chr(int(charc)) in 'Plstrwnη12346780deσπω△ρ∂pqf':
            ver = '_' + str(random.randint(1, 2))
        else:
            ver = ''  
        charcode = charc + ver
        adjustments = {
            '101_1': [0, 0.4, -0.2, -0.2], '102_1': [-0.3, 0.7, 1, 1], '103': [-0.7, -0.5, 0.5, 2.5],
            '105': [-0.3, 0.1, -0.5, -0.5], '106': [-0.7, 0.1, -0.7, 0.5], '110_1': [0, 0.4, -0.2, -0.2],
            '112_1': [0, -0.5, -0.2, 2], '113_1': [0, -0.2, -0.2, 1.2], '114_1': [0, -1.9, -0.2, 1.5],
            '116_1': [0, -2, -0.2, 2], '119_1': [0.1, 1, -0.2, -0.8], '120': [0.2, -0.8, -0.2, 0.5],
            '121': [0.2, 1.3, -0.2, 0.5], '122': [-0.2, -0.4, -0.2, 0.5], '66': [0, -0.6, -0.2, 0.5],
            '50_1': [0, -0.6, -0.2, 0.5], '100_2': [0, 0, -0.2, 0.5], '102_2': [0, 0, -0.2, 2],
            '110_2': [0, 1, -0.2, -0.2], '112_2': [0, 0.6, -0.2, 0.3], '113_2': [0, 1, -0.2, 0],
            '114_2': [0, 0.5, -0.2, -0.5], '115_2': [0, 0.8, -0.5, -0.8], '119_2': [0.1, 0.8, -0.5, -0.8],
            '97': [0, 0.4, 0, -0.5], '101_2': [0, 0.8, -0.2, -0.2], '44': [-1.6, 0.6, 0, 0],
            '87': [-0.5, -0.8, 0, 1], '107': [-0.1, -1, 0, 1], '104': [-0.1, -1, 0, 1], '108_1': [-0.6, -1, 0, 1],
            '72': [-0.7, -0.6, 0, 1], '71': [-0.7, -0.6, 0, 1], '65': [-0.7, -0.6, 0, 1], '8730': [1.5, -0.3, 4, 0.8],
            'line_3': [4.4, -0.5, 0, 1], '115_1': [-1, 0, 0, 0], '117': [-1, 0, 0, 0], '8747': [0.4, -1.7, -0.1, 4]
        }
        if charcode in adjustments.keys():
            x += adjustments[charcode][0]
            y += adjustments[charcode][1]
            w += adjustments[charcode][2]
            h += adjustments[charcode][3]
        try:
            self.image(path + f"/{charcode}.png", x=x, y=y, w=w, h=h, type='PNG')
        except:
            pass


def writepdf(textr,Outfilename):
    pdf = PDF()
    pdf.add_page()
    directory = 'handwritten3'
    pdf.image("pagec.png", x=0, y=0, w=210, h=297)

    downshift = 0
    shifter = 0
    char_index = -1
    while char_index < len(textr) - 1:
        char_index += 1
        writestat = True
        char = textr[char_index]
        if char == '√':
            mini = 0
            while textr[char_index + mini] != ' ':
                mini += 1
            if mini > 2:
                pdf.add_transparent_image(
                    f"{directory}",
                    x=10 + shifter,
                    y=10 + downshift,
                    w=mini * 3 - 4,
                    h=0,
                    charc="line_3",
                )
                shifter += 1
            else:
                pdf.add_transparent_image(
                    f"{directory}",
                    x=10 + shifter,
                    y=10 + downshift,
                    w=4,
                    h=0,
                    charc="line_3",
                )
                shifter += 1
        if char == "$":
            if textr[char_index + 1] == "^":
                writestat = False
                downshift -= 1
                char_index += 2
                while textr[char_index] != ' ':
                    pdf.add_transparent_image(
                        f"{directory}",
                        x=10 + shifter,
                        y=10 + downshift,
                        w=3,
                        h=3,
                        charc=f"{ord(textr[char_index])}"
                    )
                    char_index += 1
                    shifter += 2.2
                downshift += 1
            if textr[char_index + 1] == "_":
                writestat = False
                downshift += 3.2
                char_index += 2
                while textr[char_index] != ' ':
                    pdf.add_transparent_image(
                        f"{directory}",
                        x=10 + shifter,
                        y=10 + downshift,
                        w=3,
                        h=3,
                        charc=f"{ord(textr[char_index])}"
                    )
                    char_index += 1
                    shifter += 2.2
                downshift -= 3.2
            if textr[char_index + 1] == "s":
                writestat=False
                char_index+=1
                mini = 0
                while textr[char_index+mini] != ' ':
                    mini+=1
                pdf.add_transparent_image(f'{directory}',x=10 + shifter,y=11 + downshift,w=3*mini,h=7,charc='scratch1')
            if textr[char_index + 1] == "m":
                #making of matrix
                '''
                ~ to end matrix & to switch row and | to switch column
                '''
                
                downshift+=10
                vheight = 0
                name_ = ''
                char_index += 2
                i_ = 0
                while(textr[char_index+i_]!='~'):
                    name_+=textr[char_index+i_]
                    i_+=1
                char_index+=i_
                name_=name_.split('&')
                for i in name_:
                    shifter =0
                    for j in i.split('|'):
                        shifter+=6
                        pdf.add_transparent_image(
                            f"{directory}",
                            x=10 + shifter,
                            y=10 + downshift,
                            w=3,
                            h=3,
                            charc=f"{ord(' ')}"
                        )                    
                        for k in j:
                            shifter+=1.8
                            pdf.add_transparent_image(
                                f"{directory}",
                                x=10 + shifter,
                                y=10 + downshift,
                                w=3,
                                h=3,
                                charc=f"{ord(k)}"
                            ) 
                    downshift+=7                 
            if textr[char_index + 1] == "i":
                writestat=False
                name=''
                char_index+=1
                i_=0
                while textr[char_index+i_] != ' ':
                    name += textr[char_index]
                    i_+=1
                pdf.add_transparent_image(f'{directory}',x=10 + shifter,y=11 + downshift,w=40,h=30,charc='aspirin')
                shifter+=0
                downshift+=30
            if textr[char_index + 1] == "f":
                writestat = False
                mini=0
                cutr=0
                while textr[char_index+2+mini]!=' ':
                    if textr[char_index+2+mini] in '$_`^':
                        cutr+=1
                    mini+=1
                mini-=cutr
                mini1=0
                cutr=0
                while textr[char_index+3+mini+mini1]!=' ':
                    if textr[char_index+2+mini] in '$_`^':
                        cutr+=1
                    mini1+=1
                mini1-=cutr
                mini = max(mini,mini1)*1.2
                downshift -= 2
                char_index += 2
                ogx = shifter
                shifter+=2
                while textr[char_index] != ' ':
                    if textr[char_index] == "$":
                        if textr[char_index + 1] == "^":
                            writestat = False
                            downshift -= 1
                            char_index += 2
                            while textr[char_index] != '`':
                                pdf.add_transparent_image(
                                    f"{directory}",
                                    x=10 + shifter,
                                    y=10 + downshift,
                                    w=3,
                                    h=3,
                                    charc=f"{ord(textr[char_index])}"
                                )
                                char_index += 1
                                shifter += 2.2
                            downshift += 1
                            shifter-=2.2
                        elif textr[char_index+1] == "_":
                            writestat = False
                            downshift += 3.2
                            char_index += 2
                            while textr[char_index] != '`':
                                pdf.add_transparent_image(
                                    f"{directory}",
                                    x=10 + shifter,
                                    y=10 + downshift,
                                    w=3,
                                    h=3,
                                    charc=f"{ord(textr[char_index])}"
                                )
                                char_index += 1
                                shifter += 2.2
                            downshift -= 3.2
                            shifter-=2.2
                    else:
                        pdf.add_transparent_image(
                            f"{directory}",
                            x=10 + shifter,
                            y=10 + downshift,
                            w=3,
                            h=3,
                            charc=f"{ord(textr[char_index])}"
                        )
                        char_index += 1
                        shifter += 2.2
                downshift += 2
                shifter=ogx
                char_index+=1
                downshift += 3
                pdf.add_transparent_image(f'{directory}',x=8.5+ogx-mini,y=10+downshift-0.8,w=2.9*mini,h=0,charc="line_3")
                shifter+=1.2
                while textr[char_index] != ' ':
                    if textr[char_index] == "$":
                        if textr[char_index + 1] == "^":
                            writestat = False
                            downshift -= 1
                            char_index += 2
                            while textr[char_index] != '`':
                                pdf.add_transparent_image(
                                    f"{directory}",
                                    x=10 + shifter,
                                    y=10 + downshift,
                                    w=3,
                                    h=3,
                                    charc=f"{ord(textr[char_index])}"
                                )
                                char_index += 1
                                shifter += 2.2
                            downshift += 1
                            shifter-=2.2
                        elif textr[char_index+1] == "_":
                            writestat = False
                            downshift += 3.2
                            char_index += 2
                            while textr[char_index] != '`':
                                pdf.add_transparent_image(
                                    f"{directory}",
                                    x=10 + shifter,
                                    y=10 + downshift,
                                    w=3,
                                    h=3,
                                    charc=f"{ord(textr[char_index])}"
                                )
                                char_index += 1
                                shifter += 2.2
                            downshift -= 3.2
                            shifter-=2.2
                    else:
                        pdf.add_transparent_image(
                            f"{directory}",
                            x=10 + shifter,
                            y=10 + downshift,
                            w=3,
                            h=3,
                            charc=f"{ord(textr[char_index])}"
                        )
                        char_index += 1
                        shifter += 2.2
                downshift -= 3     
                shifter+=5
        # Handle newline
        if char == '\n':
            shifter = 0  # Reset horizontal position
            downshift += 10  # Move down to the next line
            continue

        # Determine version for specific characters
        try:
            if writestat:
                pdf.add_transparent_image(
                    f"{directory}",
                    x=10 + shifter,
                    y=10 + downshift,
                    w=4,
                    h=5,
                    charc=f"{ord(char)}"
                )
                shifter += 2.8
            writestat = True

            # Move to a new line if the current line width exceeds the page width
            if shifter >= 190:
                shifter = 0
                downshift += 10
                # Add a hyphen if the next character is alphanumeric
                if char_index + 1 < len(textr) and textr[char_index + 1].isalnum():
                    pdf.add_transparent_image(
                        f"{directory}",
                        x=10 + shifter,
                        y=10 + downshift,
                        w=4,
                        h=5,
                        charc=f"{ord('-')}"
                    )
                    shifter += 2.8

            # Add a new page if the current page is full
            if downshift >= 280:
                pdf.add_page()
                pdf.image("pagec.png", x=0, y=0, w=210, h=297)
                downshift = 0
        except FileNotFoundError:
            # Skip missing images
            pass

    pdf.output(f"{Outfilename}.pdf")