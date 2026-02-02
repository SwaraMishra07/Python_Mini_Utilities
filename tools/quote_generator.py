import random
def quote_generator():
    
      # Categories for quote generator.

    print("\n--- Random Quote Generator ---")
    print("\nPick a category number to get inspired: ")
    print("1. Motivational")
    print("2. Inspirational")
    print("3. Technology")
    print("4. Success")
    print("5. Life")
    print("6. Failure")
    
    choice =int(input("Enter choice by number: "))

    if choice==1:
        motivational_quotes=["“Success doesn’t come from what you do occasionally, it comes from what you do consistently",
                              "Push yourself, because no one else is going to do it for you.",
                              "Dream big. Start small. Act now.",
                              "Your only limit is your mindset.",
                              "Don’t stop when you’re tired. Stop when you’re done.",
                              "Hard work beats talent when talent doesn’t work hard.",
                              "Believe in yourself and all that you are.",
                              "Small steps every day lead to big results.",
                              "Discipline is choosing between what you want now and what you want most.",
                              "You are capable of more than you think."
                             ]
        print("\n Here’s a quote for you:\n")
        print(random.choice(motivational_quotes))
    elif choice==2:
        inspirational_quotes=["Every day is a new chance to become a better version of yourself.",
                               "Believe in the power of small beginnings.",
                               "Light shines brightest in moments of darkness.",
                               "Your journey matters more than the speed.",
                               "Inspiration begins the moment you refuse to give up.",
                               "Great things start with a single step forward.",
                               "You don’t need permission to chase your dreams",
                               "Hope is stronger than fear.",
                               "Growth begins where comfort ends.",
                               "Your story is still being written.",
                               ]
        print("\n Here’s a quote for you:\n")
        print(random.choice(inspirational_quotes)) 
    elif choice==3:
        tech_quotes=[ "Code is like humor. When you have to explain it, it’s bad.",
                      "First, solve the problem. Then, write the code.",
                      "Experience is the name everyone gives to their mistakes.",
                      "In theory, theory and practice are the same. In practice, they’re not.",
                      "Programs must be written for people to read, and only incidentally for machines to execute.",
                      "Debugging is twice as hard as writing the code in the first place.",
                      "Simplicity is the soul of efficiency.",
                      "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
                      "If debugging is the process of removing bugs, then programming must be the process of putting them in."
            ]
        
        print("\n Here’s a quote for you:\n")
        print(random.choice(tech_quotes)) 
    elif choice==4:
        success_quotes=["Success is built on patience, persistence, and purpose",
                        "Small consistent efforts create big achievements.",
                        "Success comes to those who prepare for it daily.",
                        "Focus on progress, not perfection.",
                        "Success is earned, not gifted.",
                        "Discipline is the bridge between goals and success.",
                        "Success is doing ordinary things extraordinarily well.",
                        "Work quietly, let success speak.",
                        "Success grows where effort flows.",
                        "Your habits decide your future.",
                        ]
        print("\n Here’s a quote for you:\n")
        print(random.choice(success_quotes))            
    elif choice==5:
        life_quotes=["Life is about learning, unlearning, and growing.",
                     "Life makes sense when you live it, not rush it.",
                     "Every moment teaches something valuable.",
                     "Life becomes easier when you accept change.",
                     "Peace comes from within, not circumstances.",
                     "Life rewards those who stay curious.",
                     "Simple moments often hold the deepest meaning.",
                     "Life is shaped by the choices you make today.",
                     "Live with intention, not hesitation.",
                     "Life isn’t perfect, but it’s meaningful."]
        print("\n Here’s a quote for you:\n")
        print(random.choice(life_quotes)) 
    elif choice==6:
        failure_quotes=["Failure is proof that you tried.",
                        "Every failure carries a lesson worth learning.",
                        "Failure is not the end, it’s feedback.",
                        "Failing means you’re moving forward.",
                        "Mistakes are steps, not setbacks.",
                        "Failure shapes strength and wisdom.",
                        "Each failure brings you closer to success.",
                        "Failure teaches what success never can.",
                        "Don’t fear failure; fear not trying.",
                        "Failure refines, not defines you."
                        ]    
        print("\n Here’s a quote for you:\n")
        print(random.choice(failure_quotes)) 



if __name__ == "__main__":
   
    quote_generator()
