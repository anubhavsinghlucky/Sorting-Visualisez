import pygame
import random
pygame.init()
pygame.mixer.init()

class DrawInfo:
    BLACK= 0,0,0
    WHITE= 255, 255, 255
    GREEN= 0, 255, 255
    RED= 255, 0, 0
    BACKGROUND_COLOR= WHITE

    GRADIENTS=[
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]
    SORT_SOUND=pygame.mixer.Sound('kick30-83325.mp3')
    SORT1_SOUND=pygame.mixer.Sound('piano-g-6200.mp3')

    SMALL_FONT= pygame.font.SysFont('comicsans',17)
    FONT = pygame.font.SysFont('comicsans',20)
    LARGE_FONT= pygame.font.SysFont('comicsans',30)

    SIDE_PAD= 0
    TOP_PAD= 150

    def __init__(self,width, height, lst):
        self.width= width
        self.height= height

        self.window= pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)
    
    def set_list(self,lst):
        self.lst = lst
        self.min_val= min(lst)
        self.max_val= max(lst) #taking max and min of the list of bars

        self.block_width= round((self.width-self.SIDE_PAD)/ len(lst))
        self.block_height= int((self.height-self.TOP_PAD)/(self.max_val-self.min_val))
        self.start_x= self.SIDE_PAD // 2

        
def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title= draw_info.LARGE_FONT.render(f"{algo_name}-{'Ascending' if ascending else 'Descending'}",1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2- title.get_width()/2, 5))

    controls= draw_info.FONT.render("R - Reset | SPACE- Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting= draw_info.SMALL_FONT.render("B - Bubble Sort | I - Insertion Sort | S - Selection Sort | H - Heap Sort | M - Merge Sort",1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info,color_positions= {}, clear_bg= False):
    lst= draw_info.lst

    if clear_bg:
        clear_rect= (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width- draw_info.SIDE_PAD, draw_info.height- draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.WHITE, clear_rect)
    for i, val in enumerate(lst):
        x= draw_info.start_x + i * draw_info.block_width
        y=draw_info.height-(val)#change
        #_y=(draw_info.height) - (val) * draw_info.block_height
        color= draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color= color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width,draw_info.height))#change
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst= []
    for _ in range(n):
        val= random.randint(min_val,max_val)
        lst.append(val)    
    return lst

def bubble_sort(draw_info, ascending= True):
    lst= draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2 = lst[j+1]
            
            if(num1>num2 and ascending) or (num1<num2 and not ascending):
                #draw_info.SORT1_SOUND.play()
                lst[j],lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j: draw_info.GREEN, j+1: draw_info.RED},True)
                yield True #pauses the execution and returns a generator
        draw_info.SORT_SOUND.play()
    return lst 
    

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
            lst[j + 1] = lst[j]
            draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
            yield True
            j -= 1
        lst[j + 1] = current
        draw_list(draw_info, {j + 1: draw_info.RED}, True)
        draw_info.SORT_SOUND.play()
    return lst

def selection_sort(draw_info,ascending=True):
    lst=draw_info.lst

    for s in range(len(lst)-1):
        min_idx = s
        for i in range(s + 1, len(lst)):
            # For sorting in descending order
            # for minimum element in each loop
            if (lst[i] < lst[min_idx]) and ascending or (lst[i] > lst[min_idx] and not ascending):
                min_idx = i
                draw_list(draw_info,{s: draw_info.GREEN,min_idx: draw_info.RED}, True)
                yield True 
        draw_info.SORT_SOUND.play()
        # Arranging min at the correct position
        if (min_idx!=s):
            (lst[s], lst[min_idx]) = (lst[min_idx], lst[s])
            draw_list(draw_info,{s: (0,200,100),min_idx: (100,200,0)}, True)
            #draw_info.SORT_SOUND.play()
    return lst

def heapify(draw_info,lst,n,i,ascending):
    largest= i
    l=2 * i + 1
    r=2 * i + 2
    if (l < n and lst[i] < lst[l] and ascending) or (l < n and lst[l] < lst[largest] and not ascending):
        largest = l
        #draw_info.SORT_SOUND.play()
    if (r < n and lst[largest] < lst[r] and ascending) or (r < n and lst[largest] > lst[r] and not ascending):
        largest = r
    if largest != i:
        (lst[i], lst[largest]) = (lst[largest], lst[i]) 
        draw_info.SORT_SOUND.play()
        draw_list(draw_info,{i: draw_info.GREEN,largest: draw_info.RED}, True)
        heapify(draw_info,lst, n, largest,ascending)

def heapSort(draw_info,ascending=True):
    lst=draw_info.lst
    n = len(lst)
    for i in range(n // 2, -1, -1):
        heapify(draw_info,lst, n, i,ascending)
    for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i]) 
        draw_list(draw_info,{0: (0,0,255),i: (0,255,0)}, True)
        heapify(draw_info,lst, i, 0,ascending)
        yield True

def merge(draw_info,a, l, m, r,ascending): 
    n1 = m - l + 1
    n2 = r - m 
    L = [0] * n1 
    R = [0] * n2 
    for i in range(0, n1): 
        L[i] = a[l + i] 
    for i in range(0, n2): 
        R[i] = a[m + i + 1] 
 
    i, j, k = 0, 0, l 
    while i < n1 and j < n2: 
        if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending): 
            a[k] = L[i]
            draw_list(draw_info,{i: draw_info.GREEN,k: draw_info.RED}, True) 
            i += 1
        else: 
            a[k] = R[j] 
            j += 1
        k += 1
 
    while i < n1: 
        a[k] = L[i] 
        draw_list(draw_info,{i: (0,200,100),k: (200,0,100)}, True)
        i += 1
        k += 1
 
    while j < n2:
        a[k] = R[j] 
        draw_list(draw_info,{k: (100,200,100),j: (200,100,100)}, True)
        j += 1
        k += 1 
 
def mergesort(draw_info,ascending=True):
    lst=draw_info.lst
    width = 1   
    n = len(lst)                                          
    while (width < n):
        l=0
        draw_info.SORT_SOUND.play()
        while (l < n): 
            r = min(l+(width*2-1), n-1)         
            m = min(l+width-1,n-1)             
            merge(draw_info,lst, l, m, r,ascending)
            draw_list(draw_info,{l: (100,200,100),r: (200,100,100)}, True)
            
            l += width*2 
        yield True
        width *= 2
    return lst

def main():
    run= True
    clock= pygame.time.Clock()

    n=input("Enter no. of inputs:")
    n=int(n)
    if n < 1 or n > 1000:
      print("Please enter a number between 1 and 1000.")
      return
    min_val = 0
    max_val = 450

    lst= generate_starting_list(n,min_val,max_val)
    draw_info= DrawInfo(1000, 600, lst)
    sorting= False
    ascending= True

    sorting_algorithm= bubble_sort
    sorting_algo_name= "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting= False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run= False

            if event.type != pygame.KEYDOWN: #no key pressed
                continue

            if event.key == pygame.K_r: #if R pressed-> Reset
                lst= generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting= False
            elif event.key== pygame.K_SPACE and sorting== False:
                sorting= True
                sorting_algorithm_generator= sorting_algorithm(draw_info,ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending= True
            elif event.key == pygame.K_d and not sorting:
                ascending= False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm= insertion_sort
                sorting_algo_name= "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm= bubble_sort
                sorting_algo_name= "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm= selection_sort
                sorting_algo_name= "Selection Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm= heapSort
                sorting_algo_name= "Heap Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm= mergesort
                sorting_algo_name= "Merge Sort"
    pygame.quit()

if __name__ == "__main__":
    main()
