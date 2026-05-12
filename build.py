#!/usr/bin/env python3
"""Compile state metadata and merge with geo data into final index.html."""
import json
import os

STATE_DATA = {
    "AL": {
        "name": "Alabama", "region": "South", "capital": "Montgomery", "pop": 5108468,
        "facts": [
            "The civil rights movement gained national attention here after the 1955 Montgomery Bus Boycott.",
            "Nicknamed the Yellowhammer State after the state bird, a yellow-shafted flicker woodpecker.",
            "NASA's Marshall Space Flight Center in Huntsville designed the Saturn V rocket that carried astronauts to the Moon."
        ],
        "neighbors": ["FL", "GA", "TN", "MS"]
    },
    "AK": {
        "name": "Alaska", "region": "West", "capital": "Juneau", "pop": 733406,
        "facts": [
            "Largest state in area — more than twice the size of Texas and bigger than the next two states combined.",
            "Purchased from Russia in 1867 for $7.2 million, about two cents per acre.",
            "Juneau is the only state capital that cannot be reached by road — only by plane or boat."
        ],
        "neighbors": []
    },
    "AZ": {
        "name": "Arizona", "region": "West", "capital": "Phoenix", "pop": 7431344,
        "facts": [
            "Home to the Grand Canyon, carved by the Colorado River over millions of years.",
            "Does not observe daylight saving time, except for the Navajo Nation.",
            "Phoenix is the fifth-largest city in the United States by population."
        ],
        "neighbors": ["CA", "NV", "UT", "CO", "NM"]
    },
    "AR": {
        "name": "Arkansas", "region": "South", "capital": "Little Rock", "pop": 3067732,
        "facts": [
            "The only US state where diamonds are mined — at Crater of Diamonds State Park you can keep what you find.",
            "Walmart was founded in Bentonville in 1962 by Sam Walton.",
            "The Ozark and Ouachita mountains give Arkansas more terrain variety than its 'flat' neighbors."
        ],
        "neighbors": ["MO", "TN", "MS", "LA", "TX", "OK"]
    },
    "CA": {
        "name": "California", "region": "West", "capital": "Sacramento", "pop": 38965193,
        "facts": [
            "Most populous US state and the fifth-largest economy in the world if it were a country.",
            "Contains both the highest (Mt. Whitney) and lowest (Death Valley) points in the contiguous United States.",
            "The 1849 Gold Rush brought 300,000 people west and gave California its 'Golden State' nickname."
        ],
        "neighbors": ["OR", "NV", "AZ"]
    },
    "CO": {
        "name": "Colorado", "region": "West", "capital": "Denver", "pop": 5877610,
        "facts": [
            "Highest average elevation of any US state at about 6,800 feet.",
            "Denver, the 'Mile-High City', sits exactly 5,280 feet above sea level.",
            "Has more than 50 'fourteeners' — peaks above 14,000 feet — more than any other state."
        ],
        "neighbors": ["WY", "NE", "KS", "OK", "NM", "AZ", "UT"]
    },
    "CT": {
        "name": "Connecticut", "region": "Northeast", "capital": "Hartford", "pop": 3617176,
        "facts": [
            "Nicknamed the Constitution State; the Fundamental Orders of 1639 are considered America's first written constitution.",
            "Hartford was the insurance capital of the world for much of the 20th century.",
            "Yale University in New Haven, founded in 1701, is the third-oldest university in the US."
        ],
        "neighbors": ["RI", "MA", "NY"]
    },
    "DE": {
        "name": "Delaware", "region": "South", "capital": "Dover", "pop": 1031890,
        "facts": [
            "The First State — first to ratify the US Constitution in 1787.",
            "More than 60% of Fortune 500 companies are incorporated here, thanks to business-friendly law.",
            "Second-smallest state by area, only about 96 miles long and 35 miles wide."
        ],
        "neighbors": ["PA", "NJ", "MD"]
    },
    "FL": {
        "name": "Florida", "region": "South", "capital": "Tallahassee", "pop": 22610726,
        "facts": [
            "Has the longest coastline in the contiguous US at about 1,350 miles.",
            "St. Augustine, founded by the Spanish in 1565, is the oldest continuously inhabited European-established settlement in the US.",
            "Home to NASA's Kennedy Space Center, where every crewed US space launch has lifted off."
        ],
        "neighbors": ["GA", "AL"]
    },
    "GA": {
        "name": "Georgia", "region": "South", "capital": "Atlanta", "pop": 11029227,
        "facts": [
            "Atlanta's Hartsfield-Jackson airport has been the busiest in the world for most of the last 25 years.",
            "Coca-Cola was invented in Atlanta in 1886 by pharmacist John Pemberton.",
            "The official state fruit is the peach, and the state nickname is the Peach State."
        ],
        "neighbors": ["FL", "AL", "TN", "NC", "SC"]
    },
    "HI": {
        "name": "Hawaii", "region": "West", "capital": "Honolulu", "pop": 1435138,
        "facts": [
            "The only US state made up entirely of islands and the only one outside North America.",
            "Most recent state to join the Union, admitted on August 21, 1959.",
            "Kīlauea on the Big Island is one of the world's most active volcanoes."
        ],
        "neighbors": []
    },
    "ID": {
        "name": "Idaho", "region": "West", "capital": "Boise", "pop": 1964726,
        "facts": [
            "Produces about a third of all potatoes grown in the United States.",
            "Hells Canyon, on the Idaho–Oregon border, is North America's deepest river gorge — deeper than the Grand Canyon.",
            "The Idaho state seal is the only US state seal designed by a woman, Emma Edwards Green, in 1891."
        ],
        "neighbors": ["WA", "OR", "NV", "UT", "WY", "MT"]
    },
    "IL": {
        "name": "Illinois", "region": "Midwest", "capital": "Springfield", "pop": 12549689,
        "facts": [
            "Abraham Lincoln spent most of his adult life here; Springfield is home to his tomb and museum.",
            "Chicago's Willis Tower (formerly Sears Tower) was the world's tallest building from 1973 to 1998.",
            "The first skyscraper, the Home Insurance Building, opened in Chicago in 1885."
        ],
        "neighbors": ["WI", "IA", "MO", "KY", "IN"]
    },
    "IN": {
        "name": "Indiana", "region": "Midwest", "capital": "Indianapolis", "pop": 6862199,
        "facts": [
            "The Indianapolis 500, run since 1911, is one of the oldest and most famous auto races in the world.",
            "Nicknamed the Hoosier State — the origin of 'Hoosier' is still debated.",
            "Indiana produces more popcorn than any other state."
        ],
        "neighbors": ["MI", "OH", "KY", "IL"]
    },
    "IA": {
        "name": "Iowa", "region": "Midwest", "capital": "Des Moines", "pop": 3207004,
        "facts": [
            "Holds the first-in-the-nation presidential caucuses, kicking off the campaign cycle every four years.",
            "Produces more corn than any other state — roughly 17% of the national crop.",
            "The only state whose east and west borders are both formed by rivers (Mississippi and Missouri)."
        ],
        "neighbors": ["MN", "WI", "IL", "MO", "NE", "SD"]
    },
    "KS": {
        "name": "Kansas", "region": "Midwest", "capital": "Topeka", "pop": 2940546,
        "facts": [
            "Geographic center of the contiguous 48 states lies near Lebanon, Kansas.",
            "The 1954 Supreme Court case Brown v. Board of Education originated in Topeka.",
            "Dorothy's home in 'The Wizard of Oz' — and yes, tornadoes are very real here."
        ],
        "neighbors": ["NE", "MO", "OK", "CO"]
    },
    "KY": {
        "name": "Kentucky", "region": "South", "capital": "Frankfort", "pop": 4526154,
        "facts": [
            "Produces 95% of the world's bourbon whiskey along the famous Bourbon Trail.",
            "Home to the Kentucky Derby, the longest-running annual sporting event in the United States (since 1875).",
            "Fort Knox holds much of the United States' gold reserves."
        ],
        "neighbors": ["IL", "IN", "OH", "WV", "VA", "TN", "MO"]
    },
    "LA": {
        "name": "Louisiana", "region": "South", "capital": "Baton Rouge", "pop": 4573749,
        "facts": [
            "The only US state where law is partly based on the Napoleonic Code rather than English common law.",
            "Subdivided into parishes instead of counties — a legacy of French and Spanish colonial rule.",
            "New Orleans hosts the country's largest Mardi Gras celebration each year."
        ],
        "neighbors": ["TX", "AR", "MS"]
    },
    "ME": {
        "name": "Maine", "region": "Northeast", "capital": "Augusta", "pop": 1395722,
        "facts": [
            "Produces over 90% of the lobster caught in the United States.",
            "The only US state whose name is a single syllable.",
            "Acadia National Park's Cadillac Mountain is among the first places in the country to see sunrise each day."
        ],
        "neighbors": ["NH"]
    },
    "MD": {
        "name": "Maryland", "region": "South", "capital": "Annapolis", "pop": 6180253,
        "facts": [
            "Donated the land that became Washington, D.C. in 1790.",
            "Annapolis served as the temporary US capital in 1783–84 and is home to the US Naval Academy.",
            "The Star-Spangled Banner was written in 1814 at Fort McHenry in Baltimore."
        ],
        "neighbors": ["DE", "PA", "WV", "VA"]
    },
    "MA": {
        "name": "Massachusetts", "region": "Northeast", "capital": "Boston", "pop": 7001399,
        "facts": [
            "The Pilgrims landed at Plymouth in 1620, founding one of America's earliest English colonies.",
            "Harvard, founded in 1636, is the oldest institution of higher education in the United States.",
            "The first shots of the Revolutionary War were fired at Lexington and Concord in 1775."
        ],
        "neighbors": ["NH", "VT", "NY", "CT", "RI"]
    },
    "MI": {
        "name": "Michigan", "region": "Midwest", "capital": "Lansing", "pop": 10037261,
        "facts": [
            "The only state split into two non-contiguous peninsulas, divided by the Straits of Mackinac.",
            "Touches four of the five Great Lakes — Superior, Michigan, Huron, and Erie.",
            "Detroit is the birthplace of the modern auto industry; Henry Ford's assembly line debuted here in 1913."
        ],
        "neighbors": ["OH", "IN", "WI"]
    },
    "MN": {
        "name": "Minnesota", "region": "Midwest", "capital": "Saint Paul", "pop": 5737915,
        "facts": [
            "Known as the Land of 10,000 Lakes — there are actually about 11,842 lakes of 10+ acres.",
            "The Mississippi River begins at Lake Itasca in northern Minnesota.",
            "The Mall of America in Bloomington is one of the largest shopping malls in the world."
        ],
        "neighbors": ["WI", "IA", "SD", "ND"]
    },
    "MS": {
        "name": "Mississippi", "region": "South", "capital": "Jackson", "pop": 2939690,
        "facts": [
            "The Delta region is widely considered the birthplace of the blues.",
            "Elvis Presley was born in Tupelo in 1935.",
            "The state was named after the Mississippi River, whose name comes from an Ojibwe word for 'great river'."
        ],
        "neighbors": ["LA", "AR", "TN", "AL"]
    },
    "MO": {
        "name": "Missouri", "region": "Midwest", "capital": "Jefferson City", "pop": 6196156,
        "facts": [
            "The Gateway Arch in St. Louis is the tallest monument in the United States at 630 feet.",
            "The Lewis and Clark Expedition launched from St. Louis in 1804.",
            "Missouri borders eight states — tied with Tennessee for the most of any state."
        ],
        "neighbors": ["IA", "IL", "KY", "TN", "AR", "OK", "KS", "NE"]
    },
    "MT": {
        "name": "Montana", "region": "West", "capital": "Helena", "pop": 1132812,
        "facts": [
            "Nicknamed Big Sky Country for its vast, open landscapes.",
            "Home to Glacier National Park, which sits on the Continental Divide near Canada.",
            "The Battle of the Little Bighorn — Custer's Last Stand — took place here in 1876."
        ],
        "neighbors": ["ND", "SD", "WY", "ID"]
    },
    "NE": {
        "name": "Nebraska", "region": "Midwest", "capital": "Lincoln", "pop": 1978379,
        "facts": [
            "The only state with a unicameral (single-house) and officially nonpartisan legislature.",
            "Warren Buffett's company Berkshire Hathaway is headquartered in Omaha.",
            "Arbor Day, the national tree-planting holiday, was founded in Nebraska City in 1872."
        ],
        "neighbors": ["SD", "IA", "MO", "KS", "CO", "WY"]
    },
    "NV": {
        "name": "Nevada", "region": "West", "capital": "Carson City", "pop": 3194176,
        "facts": [
            "More than 80% of the state is owned by the federal government — the highest percentage in the US.",
            "Las Vegas wasn't a major city until the Hoover Dam construction project brought workers in the 1930s.",
            "Driest state in the country, averaging less than 10 inches of rainfall a year."
        ],
        "neighbors": ["OR", "ID", "UT", "AZ", "CA"]
    },
    "NH": {
        "name": "New Hampshire", "region": "Northeast", "capital": "Concord", "pop": 1402054,
        "facts": [
            "Holds the first presidential primary every four years.",
            "State motto 'Live Free or Die' is one of the most famous in the country.",
            "Mount Washington has recorded some of the highest surface wind speeds ever observed (231 mph in 1934)."
        ],
        "neighbors": ["VT", "MA", "ME"]
    },
    "NJ": {
        "name": "New Jersey", "region": "Northeast", "capital": "Trenton", "pop": 9290841,
        "facts": [
            "Most densely populated US state, with about 1,260 people per square mile.",
            "Thomas Edison's lab in Menlo Park gave us the phonograph, light bulb, and motion picture camera.",
            "Has more diners than any other state, earning it the unofficial title 'Diner Capital of the World'."
        ],
        "neighbors": ["NY", "PA", "DE"]
    },
    "NM": {
        "name": "New Mexico", "region": "West", "capital": "Santa Fe", "pop": 2114371,
        "facts": [
            "Santa Fe, founded in 1610, is the oldest US state capital.",
            "The first atomic bomb was detonated at the Trinity Site in the Jornada del Muerto desert on July 16, 1945.",
            "State flag — the red Zia sun on a yellow field — is regularly ranked as one of America's most beautiful."
        ],
        "neighbors": ["CO", "OK", "TX", "AZ", "UT"]
    },
    "NY": {
        "name": "New York", "region": "Northeast", "capital": "Albany", "pop": 19571216,
        "facts": [
            "New York City was the first US capital under the new Constitution from 1789 to 1790.",
            "The Statue of Liberty, dedicated in 1886, was a gift from France for the country's centennial.",
            "Niagara Falls, on the Canadian border, sends about 750,000 gallons of water over the edge every second."
        ],
        "neighbors": ["VT", "MA", "CT", "NJ", "PA"]
    },
    "NC": {
        "name": "North Carolina", "region": "South", "capital": "Raleigh", "pop": 10835491,
        "facts": [
            "Site of the Wright brothers' first powered flight at Kitty Hawk on December 17, 1903.",
            "Research Triangle (Raleigh–Durham–Chapel Hill) is one of the largest research parks in the world.",
            "Produces about half of the nation's sweet potatoes."
        ],
        "neighbors": ["VA", "TN", "GA", "SC"]
    },
    "ND": {
        "name": "North Dakota", "region": "Midwest", "capital": "Bismarck", "pop": 783926,
        "facts": [
            "The Bakken oil field made North Dakota briefly the second-largest US oil producer in the 2010s.",
            "Theodore Roosevelt ranched here in the 1880s and credited the experience with shaping his conservationist views.",
            "The geographic center of North America lies near Rugby, North Dakota."
        ],
        "neighbors": ["MT", "SD", "MN"]
    },
    "OH": {
        "name": "Ohio", "region": "Midwest", "capital": "Columbus", "pop": 11785935,
        "facts": [
            "Birthplace of seven US presidents — sometimes called the 'Mother of Presidents'.",
            "Cleveland is home to the Rock and Roll Hall of Fame.",
            "Astronauts Neil Armstrong and John Glenn were both Ohioans."
        ],
        "neighbors": ["MI", "IN", "KY", "WV", "PA"]
    },
    "OK": {
        "name": "Oklahoma", "region": "South", "capital": "Oklahoma City", "pop": 4053824,
        "facts": [
            "The 1889 Land Rush opened roughly two million acres to settlers in a single day.",
            "Sits in 'Tornado Alley' and has more tornadoes per square mile than any other state.",
            "Headquarters of 38 federally recognized Native American tribes."
        ],
        "neighbors": ["KS", "MO", "AR", "TX", "NM", "CO"]
    },
    "OR": {
        "name": "Oregon", "region": "West", "capital": "Salem", "pop": 4233358,
        "facts": [
            "Crater Lake, formed when Mount Mazama collapsed about 7,700 years ago, is the deepest lake in the US.",
            "One of only two states (with New Jersey) where it's illegal to pump your own gas in many areas.",
            "The Oregon Trail ended in the Willamette Valley, bringing tens of thousands of settlers in the 1840s–60s."
        ],
        "neighbors": ["WA", "ID", "NV", "CA"]
    },
    "PA": {
        "name": "Pennsylvania", "region": "Northeast", "capital": "Harrisburg", "pop": 12961683,
        "facts": [
            "Both the Declaration of Independence (1776) and the Constitution (1787) were signed in Philadelphia.",
            "The Battle of Gettysburg in 1863 was the bloodiest single battle of the Civil War.",
            "Hershey, the 'Chocolate Capital of the United States', was built by Milton Hershey around his factory."
        ],
        "neighbors": ["NY", "NJ", "DE", "MD", "WV", "OH"]
    },
    "RI": {
        "name": "Rhode Island", "region": "Northeast", "capital": "Providence", "pop": 1095962,
        "facts": [
            "Smallest US state by area — about 48 miles long and 37 miles wide.",
            "Officially named the 'State of Rhode Island and Providence Plantations' until a 2020 vote shortened it.",
            "First of the Thirteen Colonies to declare independence from Britain, on May 4, 1776."
        ],
        "neighbors": ["CT", "MA"]
    },
    "SC": {
        "name": "South Carolina", "region": "South", "capital": "Columbia", "pop": 5373555,
        "facts": [
            "The first state to secede from the Union in December 1860, triggering the Civil War.",
            "The first shots of the Civil War were fired at Fort Sumter in Charleston Harbor in April 1861.",
            "Produces more peaches than Georgia, despite Georgia's 'Peach State' nickname."
        ],
        "neighbors": ["NC", "GA"]
    },
    "SD": {
        "name": "South Dakota", "region": "Midwest", "capital": "Pierre", "pop": 919318,
        "facts": [
            "Mount Rushmore's four presidential heads — Washington, Jefferson, Roosevelt, Lincoln — were carved from 1927 to 1941.",
            "The Black Hills are sacred to the Lakota people and were the site of an 1870s gold rush.",
            "Pierre is one of only four US state capitals not served by an Interstate highway."
        ],
        "neighbors": ["ND", "MN", "IA", "NE", "WY", "MT"]
    },
    "TN": {
        "name": "Tennessee", "region": "South", "capital": "Nashville", "pop": 7126489,
        "facts": [
            "Nashville is known as 'Music City' and is the heart of the country music industry.",
            "Memphis was home to Elvis Presley's Graceland and the origin of rock 'n' roll at Sun Records.",
            "Borders eight states — tied with Missouri for the most of any state."
        ],
        "neighbors": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"]
    },
    "TX": {
        "name": "Texas", "region": "South", "capital": "Austin", "pop": 30503301,
        "facts": [
            "Second-largest state by both area and population, and was an independent republic from 1836 to 1845.",
            "NASA's Johnson Space Center in Houston has been the home of US human spaceflight since the 1960s.",
            "The state has its own power grid, separate from the rest of the continental US."
        ],
        "neighbors": ["NM", "OK", "AR", "LA"]
    },
    "UT": {
        "name": "Utah", "region": "West", "capital": "Salt Lake City", "pop": 3417734,
        "facts": [
            "More than 60% of Utahns are members of The Church of Jesus Christ of Latter-day Saints.",
            "The Great Salt Lake is the largest saltwater lake in the Western Hemisphere.",
            "Hosted the 2002 Winter Olympics in Salt Lake City."
        ],
        "neighbors": ["ID", "WY", "CO", "NM", "AZ", "NV"]
    },
    "VT": {
        "name": "Vermont", "region": "Northeast", "capital": "Montpelier", "pop": 647464,
        "facts": [
            "Montpelier is the least-populous US state capital, with around 8,000 residents.",
            "Produces about half of the maple syrup made in the United States.",
            "The only New England state without an Atlantic coastline."
        ],
        "neighbors": ["NY", "MA", "NH"]
    },
    "VA": {
        "name": "Virginia", "region": "South", "capital": "Richmond", "pop": 8715698,
        "facts": [
            "Birthplace of eight US presidents, more than any other state.",
            "Jamestown, founded in 1607, was the first permanent English settlement in the Americas.",
            "Richmond served as the capital of the Confederacy during most of the Civil War."
        ],
        "neighbors": ["MD", "WV", "KY", "TN", "NC"]
    },
    "WA": {
        "name": "Washington", "region": "West", "capital": "Olympia", "pop": 7812880,
        "facts": [
            "Only US state named after a president.",
            "Headquarters of Microsoft, Amazon, Starbucks, and Boeing's commercial aircraft division.",
            "Mount Rainier, an active volcano, looms 14,411 feet over the Seattle skyline."
        ],
        "neighbors": ["ID", "OR"]
    },
    "WV": {
        "name": "West Virginia", "region": "South", "capital": "Charleston", "pop": 1770071,
        "facts": [
            "Broke away from Virginia in 1863 to remain in the Union during the Civil War.",
            "The New River Gorge Bridge was the longest steel arch bridge in the world when built in 1977.",
            "Roughly 75% of the state is forested — among the highest percentages in the US."
        ],
        "neighbors": ["PA", "MD", "VA", "KY", "OH"]
    },
    "WI": {
        "name": "Wisconsin", "region": "Midwest", "capital": "Madison", "pop": 5910955,
        "facts": [
            "Produces more cheese than any other state — about a quarter of the US total.",
            "Nicknamed America's Dairyland; the official state beverage is milk.",
            "Frank Lloyd Wright was born in Richland Center and designed Taliesin in Spring Green."
        ],
        "neighbors": ["MN", "IA", "IL", "MI"]
    },
    "WY": {
        "name": "Wyoming", "region": "West", "capital": "Cheyenne", "pop": 584057,
        "facts": [
            "Least-populous US state, with fewer people than the city of Boston.",
            "Yellowstone, established in 1872 and mostly in Wyoming, was the world's first national park.",
            "First territory or state in the US to grant women the right to vote, in 1869."
        ],
        "neighbors": ["MT", "SD", "NE", "CO", "UT", "ID"]
    },
}

assert len(STATE_DATA) == 50, f"expected 50 states, got {len(STATE_DATA)}"

# Verify each state has all required fields
for code, s in STATE_DATA.items():
    for k in ("name", "region", "capital", "pop", "facts", "neighbors"):
        assert k in s, f"{code} missing {k}"
    assert len(s["facts"]) == 3, f"{code} expects 3 facts, got {len(s['facts'])}"

# Load geo
with open("paths.json") as f:
    geo = json.load(f)
geo["paths"].pop("DC", None)
geo["centroids"].pop("DC", None)
assert len(geo["paths"]) == 50

# Load template
with open("index.template.html") as f:
    tpl = f.read()

geo_json = json.dumps(geo, separators=(",", ":"))
state_json = json.dumps(STATE_DATA, separators=(",", ":"), ensure_ascii=False)

# Substitute
out = tpl.replace("__GEO_DATA__", geo_json).replace("__STATE_DATA__", state_json)

with open("index.html", "w") as f:
    f.write(out)

print(f"Built index.html: {os.path.getsize('index.html'):,} bytes")
print(f"  geo data: {len(geo_json):,} bytes")
print(f"  state data: {len(state_json):,} bytes")
