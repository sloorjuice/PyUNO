# Importing Image class from PIL module
from PIL import Image
 
# Opens a image in RGB mode
im = Image.open("images\\UNO_cards_deck.png")
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
for col in range(5):
    for row in range(14):
        # Setting the points for cropped image
        card_width = width / 14
        card_height = height / 8

        left = row  * card_width
        top = col * card_height
        right = (row + 1) * card_width
        bottom = (col + 1) * card_height
    
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))
        
        # Shows the image in image viewer
                
        if col == 0:
            if row < 10:
                im1.save(f"images\\red_{row }.png")
            elif row == 10:
                im1.save(f"images\\red_skip.png")
            elif row == 11:
                im1.save(f"images\\red_reverse.png")
            elif row == 12:
                im1.save(f"images\\red_plustwo.png")
            elif row  == 13:
                im1.save(f"images\\wild_wild.png")
        elif col == 1:
            if row < 10:
                im1.save(f"images\\yellow_{row }.png")
            elif row == 10:
                im1.save(f"images\\yellow_skip.png")
            elif row == 11:
                im1.save(f"images\\yellow_reverse.png")
            elif row == 12:
                im1.save(f"images\\yellow_plustwo.png")
        elif col == 2:
            if row < 10:
                im1.save(f"images\\green_{row }.png")
            elif row == 10:
                im1.save(f"images\\green_skip.png")
            elif row == 11:
                im1.save(f"images\\green_reverse.png")
            elif row == 12:
                im1.save(f"images\\green_plustwo.png")
        elif col == 3:
            if row < 10:
                im1.save(f"images\\blue_{row }.png")
            elif row == 10:
                im1.save(f"images\\blue_skip.png")
            elif row == 11:
                im1.save(f"images\\blue_reverse.png")
            elif row == 12:
                im1.save(f"images\\blue_plustwo.png")
        
        if col == 4:
            if row  == 13:
                im1.save(f"images\\wild_draw4.png")
            
            
        