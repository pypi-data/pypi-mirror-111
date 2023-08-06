from colorama import Fore, Style
import sys
from sylo.models import Durations


def print_welcome():
    print(f'''{Fore.RED}                               
                  #%                        
          ,//(/*****/***/((##/              
      ,//////*      /.   ,//((((((          
    //////**    .           *(((((((,       
   (/////**   {Fore.YELLOW}%@@.{Style.RESET_ALL}     {Fore.YELLOW}@@@{Style.RESET_ALL}{Fore.RED}    *((((////      
  ,(//////*,      .*/,      ./((((///(      
  .(((///////*,,**,,*/////(#((((((((##      
   #(((((///////(/////(((////((((####/      
    ###(((((((.,/((##((*  /((((#####/       
     .######((/.      ...,######%%#         
        (%#######,.  .,#####%#%%*           
             .(%%%%%%%%%%#(.                
    
SYLO - A pomodoro timer for the terminal{Style.RESET_ALL}
    ''')


def print_message(message: str, timer_val: int = None):

    if message == 'work_start':
        sys.stdout.write("\033[K")
        print(
            f'{Fore.RED}WORK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes',
            end="\r",
            flush=True
        )
    elif message == 'work_stop':
        sys.stdout.write("\033[K")
        print(
            f'{Fore.GREEN}WORK COMPLETED {Style.RESET_ALL}',
            end="\r",
            flush=True
        )
    elif message == 'work_countdown':
        sys.stdout.write("\033[K")
        print(
            f'{Fore.RED}WORK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} more seconds',
            end="\r",
            flush=True
        )
    elif message == 'break_start':
        sys.stdout.write("\033[K")
        print(
            f'Take a {Fore.GREEN}BREAK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes',
            end="\r",
            flush=True
        )
    elif message == 'break_stop':
        sys.stdout.write("\033[K")
        print(
            f'{Fore.RED}BREAK OVER{Style.RESET_ALL}',
            end="\r",
            flush=True
        )
    elif message == 'break_countdown':
        sys.stdout.write("\033[K")
        print(
            f'Take a {Fore.GREEN}BREAK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} more seconds',
            end="\r",
            flush=True
        )


def print_update(durations: Durations):
    print(f'''
Work length:        {Fore.RED}{durations.work_mins} minutes{Style.RESET_ALL}
Break length:       {Fore.GREEN}{durations.break_mins} minutes{Style.RESET_ALL}
Total work time:    {Fore.YELLOW}{durations.total_mins} minutes{Style.RESET_ALL}

Press ENTER to start the timer or Q to exit
    ''')
