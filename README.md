# **CHIP-8 Emulator in Python** `Task 1`  

## **Overview**  
This Python program implements a simple CHIP-8 emulator using `pygame` for graphical output and `numpy` for efficient memory and display management. The emulator can process basic CHIP-8 instructions and render graphics to a window.  

---

## **Code Breakdown**  

### **1. Initialization (`__init__` method)**  
When an instance of the `Chip8` class is created, the following components are initialized:  
- **Memory (`self.memory`)**: A 4KB memory space, where the first 512 bytes (0x000 to 0x1FF) are reserved for the interpreter, and programs start at address `0x200`.  
- **Registers (`self.V`)**: 16 general-purpose 8-bit registers (`V0` to `VF`), where `VF` is also used as a flag register.  
- **Display (`self.display`)**: A 64x32 monochrome pixel matrix to store graphics.  
- **Program Counter (`self.pc`)**: Set to `0x200` where CHIP-8 programs begin execution.  
- **Running State (`self.running`)**: A flag to control the main execution loop.  
- **Sprite Data**: The program loads a simple 5-byte sprite (a square) into memory at `0x300`.  
- **`pygame` Setup**: Initializes a window scaled by a factor of `10x` for better visibility.  
- **Opcode Execution**: Executes an example opcode (`0xD015`) for drawing a sprite.  

---

### **2. Opcode Execution (`execute_opcode` method)**  
The method processes CHIP-8 opcodes:  
- **`0x00E0` (CLS - Clear Screen)**: Clears the display.  
- **`0xDXYN` (Draw Sprite)**: Draws a sprite at coordinates `(Vx, Vy)`, taking `N` bytes from memory.  
  - Iterates over each row of the sprite.  
  - Extracts each pixel and XORs it with the display.  
  - If a pixel is erased, `VF` is set to `1` (collision detection).  

---

### **3. Rendering (`draw_screen` method)**  
- The screen is cleared and redrawn every frame.  
- Pixels in the display array are converted into white squares using `pygame.draw.rect()`.  
- The display is updated using `pygame.display.flip()`.  

---

### **4. Main Execution Loop (`run` method)**  
- The program continuously listens for events (e.g., quitting).  
- Calls `draw_screen()` to refresh the display at 60 FPS.  
- Stops execution when the window is closed.  

---

## **Execution Flow**  
1. An instance of `Chip8` is created (`chip8 = Chip8()`).  
2. The program initializes memory, registers, and display.  
3. The opcode `0xD015` executes, drawing a sprite on the screen.  
4. The emulator enters the main loop (`chip8.run()`).  
5. The screen updates at 60 FPS until the user closes the window.  

---

## **Future Improvements**  
- Implement a full opcode set for complete CHIP-8 functionality.  
- Add keyboard input handling for CHIP-8 programs.  
- Load and execute CHIP-8 ROMs dynamically.  
- Implement proper timing control for better emulation accuracy.  


---

# **Jarvis - The discord bot** `Task 2`
### *The Discord bot that assists you more than anyone!*  
Designed while keeping in mind the requirements of Task 2, Jarvis is here to help.  

---

## **What Can It Do?**  
From having a simple conversation to writing notes, Jarvis assists you like no one else.  

### **Core Functions:**  

### **Conversation**  
- `!c your_message`  
  - Talk to Jarvis like a friend.  
  - It remembers everything – every conversation, every fact you share.  

**Example:**  
```python
!c Hey Jarvis, how are you?  
Jarvis: I'm good! How about you?  
```

### **Reminders**  
- `!remind reminder`  
  - Have a busy schedule? No problem.
  - Jarvis will remind you both before and on time for any task.

**Example:**  
```python
!remind 09-03-2025 21:30 | Interview  
Jarvis: Reminder set for "Meeting with team at 5 PM".  
```

### **Polls**  
- `!poll question | option 1 | option 2`  
  - Want to gather opinions without manually creating a poll?
  - Just use this command, and a poll will be set up instantly.

**Example:**  
```python
!poll Which programming language do you prefer? | Python | C++ | C | Java
```

### **Music**  
- `To be added`  

### **Notes & Storage**  
- `!add your_message`  
  - Store messages, short notes, or even long paragraphs.
  - Too long to type? Just upload a .txt file.

**Example:**  
```python
!add Grocery list: Milk, Eggs, Bread  
Jarvis: Message saved: Grocery list: Milk, Eggs, Bread
```

### **Help & Queries**  
- `!ask your_query`  
  - Not sure how to use Jarvis?
  - Just ask, and it will guide you.

**Example:**  
```python
!ask How do I set a reminder?  
Jarvis: Use the command `!remind your_task` to set a reminder.  
```

### **Delete Stored Messages**  
- `!delete message_id`  
  - Removes specific stored messages you no longer need.

**Example:**  
```python
!delete 1234  
Jarvis: Message with ID 1234 has been deleted.  
```

### **UPI Registration**  
- `!upi upi_id`  
  - Register or update your UPI ID for easy access.

**Example:**  
```python
!upi smtg@smtg  
Jarvis: Notification: UPI ID updated for 13453205253130
```

### **View All Stored Messages**  
- `!show`  
  - Displays all your stored messages.

**Example:**  
```python
!show  
Jarvis:  
1. Grocery list: Milk, Eggs, Bread  
2. Meeting with team at 5 PM 
```

### **User Statistics**  
- `!stat`  
  - Provides insights about your account.

**Example:**  
```python
!stat  
Jarvis: 
+---------+------------------------+
| Field   | Value                  |
+=========+========================+
| User    | <@134502453130>        |
+---------+------------------------+
| UPI ID  | smtg@smtg              |
+---------+------------------------+
| Balance | 19992                  |
+---------+------------------------+
```

### **Generate Handwritten PDFs**  
- `!generatepdf message_id`  
  - Need to submit a handwritten-style PDF of an assignment?
  - Just one command, and your PDF is ready.

**Example:**  
```python
!generatepdf 5678  
Jarvis: <gives the pdf>  
```

`Note` Jarvis is still evolving and we will come back with more features, till then stay tuned.
