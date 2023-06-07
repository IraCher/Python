import mysql.connector
from mysql.connector import connect,Error
import pygame


def create_connection():
    try:
        with connect(host="localhost", user="root", password="Irinasuper", database="tetris") \
                as connection:
            print(connection)
            select_users = "SELECT nickname,score_max FROM users order by score_max desc"
            users = execute_read_query(connection, select_users)
            return users
    except Error as e:
        print(e)
def execute_read_query(connection, select_users):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_users)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_score(score):
    try:
        with connect(host="localhost", user="root", password="Irinasuper", database="tetris") \
                as connection:
            cursor = connection.cursor()
            query = "INSERT users (nickname,score_max) VALUES('Гость','",score,"')"
            try:
                cursor.execute(query)
                connection.commit()
                print("Query executed successfully")
            except Error as e:
                print(f"The error '{e}' occurred")
    except Error as e:
        print(e)

class bd:
    def create_records(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_records(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_records(self, surface, color, length, height, x, y, width):
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface



