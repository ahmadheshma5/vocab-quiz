from pathlib import Path
import json
from deep_translator import GoogleTranslator
raw_words = r"""
carry on
hand sth in
look after sb/sth
put sth off 
choice
choose
complain
complaint
decide
decision
deliver
delivery
describe
description
enjoy
enjoyment
explain
explanation
queue
queue (up)
change sb's mind
exchange
refund
replace
return
right away
sorry
go round
break up
come round
feel like sth
join in
pass sth on
turn sth down 
action film
bookshop
film poster
science fiction
soundtrack
accidentally
amazingly
as expected
by chance
fortunately
luckily
on purpose
surprisingly
unfortunately
down the corridor
downstairs
on the (second) floor
over there
round the corner
straight ahead
take the lift
through
address book
bookshelf
bread knife
car door
car park
city centre
coffee cup
computer game
computer screen
key ring
kitchen door
mountain climbing
mountaintop
rock climbing
shoe shop 
shopping centre
teabag
teacup
television programme
TV screen
TV star
video game
bottle top
cash machine
kitchen knife
road sign
rock star
shopping bag
street light
ticket office
bee
camel
gorilla
mosquito
parrot
spider
tiger
whale
definitely
disagree
exactly
right
true
confident
creative
easygoing
fair
fun
patient
serious
shy
sociable
strict
anxious
careless
funny
generous
honest
reliable
selfish
sensible
air pollution
local residents
parking space
public transport
quality of life
traffic congestion
urban development
cast
script
shot
soundtrack
attic
basement
bungalow
cellar
chimney
cottage
detached
fence
passage
semi-detached
terrace
terraced house
broadcast
capture
cut
editor
episode
presenter
release
series
award a grant
budget
debit an account
debt
donate to a charity
donation
finance a project
income
interest rate
investment
make a living
pay sth off
put aside savings
savings
bribe
bribery
burglar
burglary
burgle
cheat
cheat
cheating
kidnap
kidnapper
kidnapping
liar
lie
lying
murder
murder
murderer
rob
robber
robbery
shoplift
shoplifter
shoplifting
steal
theft
thief
accuse sb of sth
arrest
break into sth
court
give evidence
guilty
judge
jury
sentence
trial
verdict
witness
demolish               
clue 
cryptic 
dominate 
elegant 
urge                     
symbolize          
adorn 
gorgeous 
ominous 
monitor        
beneficial          
pursue 
solitary 
terminate 
negligible             
grip                      
thrive 
summit 
warn 
innate
notorious
plausible
quest
remote
abandon
mar
dire
mend
futile
fasten 
fundamental 
immense 
splendid
reckless 
prevail 
overcome 
crucail 
trait 
tendious
anxious 
infinite 
intense 
refine
attain
grueling 
harmful 
lack 
linger 
peril
variable
dwell
candid
objective 
roam
overwhelm
lag
relish
liable
stray
"""
words = [w.strip() for w in raw_words.splitlines() if w.strip()]

translator = GoogleTranslator(source="en", target="ar")

data = []

for w in words:
    try:
        ar = translator.translate(w)
    except Exception:
        ar = ""
    data.append({
        "english": w,
        "arabic": ar
    })

output_path = Path("words.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} words to {output_path}")
