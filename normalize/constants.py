"""Constants"""

POLYMARKET_URL = "https://polymarket.com/event/"


NBA_TEAM_MAPPING = {
    # Atlanta
    "ATL": "Hawks",
    "Atlanta": "Hawks",
    # Boston
    "BOS": "Celtics",
    "Boston": "Celtics",
    # Brooklyn
    "BKN": "Nets",
    "Brooklyn": "Nets",
    # Charlotte
    "CHA": "Hornets",
    "Charlotte": "Hornets",
    # Chicago
    "CHI": "Bulls",
    "Chicago": "Bulls",
    # Cleveland
    "CLE": "Cavaliers",
    "Cleveland": "Cavaliers",
    # Dallas
    "DAL": "Mavericks",
    "Dallas": "Mavericks",
    # Denver
    "DEN": "Nuggets",
    "Denver": "Nuggets",
    # Detroit
    "DET": "Pistons",
    "Detroit": "Pistons",
    # Golden State
    "GSW": "Warriors",
    "Golden State": "Warriors",
    # Houston
    "HOU": "Rockets",
    "Houston": "Rockets",
    # Indiana
    "IND": "Pacers",
    "Indiana": "Pacers",
    # Los Angeles teams
    "Los Angeles C": "Clippers",
    "LAC": "Clippers",
    "Los Angeles L": "Lakers",
    "LAL": "Lakers",
    # Memphis
    "MEM": "Grizzlies",
    "Memphis": "Grizzlies",
    # Miami
    "MIA": "Heat",
    "Miami": "Heat",
    # Milwaukee
    "MIL": "Bucks",
    "Milwaukee": "Bucks",
    # Minnesota
    "MIN": "Timberwolves",
    "Minnesota": "Timberwolves",
    # New Orleans
    "NOP": "Pelicans",
    "New Orleans": "Pelicans",
    # New York
    "New York K": "Knicks",
    "NYK": "Knicks",
    # Oklahoma City
    "OKC": "Thunder",
    "Oklahoma City": "Thunder",
    # Orlando
    "ORL": "Magic",
    "Orlando": "Magic",
    # Philadelphia
    "PHI": "76ers",
    "Philadelphia": "76ers",
    # Phoenix
    "PHX": "Suns",
    "Phoenix": "Suns",
    # Portland
    "POR": "Trail Blazers",
    "Portland": "Trail Blazers",
    "TrailBlazers": "Trail Blazers",
    # Sacramento
    "SAC": "Kings",
    "Sacramento": "Kings",
    # San Antonio
    "SAS": "Spurs",
    "San Antonio": "Spurs",
    # Toronto
    "TOR": "Raptors",
    "Toronto": "Raptors",
    # Washington
    "WAS": "Wizards",
    "Washington": "Wizards",
}


NHL_TEAM_MAPPING = {
    # Anaheim
    "ANA": "Ducks",
    "Anaheim": "Ducks",
    # Arizona
    "ARI": "Coyotes",
    "Arizona": "Coyotes",
    # Boston
    "BOS": "Bruins",
    "Boston": "Bruins",
    # Buffalo
    "BUF": "Sabres",
    "Buffalo": "Sabres",
    # Calgary
    "CAL": "Flames",
    "CGY": "Flames",
    "Calgary": "Flames",
    # Carolina
    "CAR": "Hurricanes",
    "Carolina": "Hurricanes",
    # Chicago
    "CHI": "Blackhawks",
    "Chicago": "Blackhawks",
    # Colorado
    "COL": "Avalanche",
    "Colorado": "Avalanche",
    # Columbus
    "CBJ": "Blue Jackets",
    "Columbus": "Blue Jackets",
    "BlueJackets": "Blue Jackets",
    # Dallas
    "DAL": "Stars",
    "Dallas": "Stars",
    # Detroit
    "DET": "Red Wings",
    "Detroit": "Red Wings",
    "RedWings": "Red Wings",
    # Edmonton
    "EDM": "Oilers",
    "Edmonton": "Oilers",
    # Florida
    "FLA": "Panthers",
    "Florida": "Panthers",
    # Los Angeles Kings
    "LA": "Kings",
    "LAK": "Kings",
    "Los Angeles": "Kings",
    # Minnesota
    "MIN": "Wild",
    "Minnesota": "Wild",
    # Montreal
    "MON": "Canadiens",
    "MTL": "Canadiens",
    "Montreal": "Canadiens",
    # Nashville
    "NSH": "Predators",
    "Nashville": "Predators",
    # New Jersey
    "NJ": "Devils",
    "NJD": "Devils",
    "New Jersey": "Devils",
    # New York Islanders
    "NYI": "Islanders",
    # New York Rangers
    "NYR": "Rangers",
    # Ottawa
    "OTT": "Senators",
    "Ottawa": "Senators",
    # Philadelphia
    "PHI": "Flyers",
    "Philadelphia": "Flyers",
    # Pittsburgh
    "PIT": "Penguins",
    "Pittsburgh": "Penguins",
    # San Jose
    "SJ": "Sharks",
    "SJS": "Sharks",
    "San Jose": "Sharks",
    # Seattle
    "SEA": "Kraken",
    "Seattle": "Kraken",
    # St. Louis
    "STL": "Blues",
    "St. Louis": "Blues",
    # Tampa Bay
    "TB": "Lightning",
    "TBL": "Lightning",
    "Tampa": "Lightning",
    "Tampa Bay": "Lightning",
    # Toronto
    "TOR": "Maple Leafs",
    "Toronto": "Maple Leafs",
    "MapleLeafs": "Maple Leafs",
    # Utah
    "UTA": "Utah",
    "Utah": "Utah",
    # Vancouver
    "VAN": "Canucks",
    "Vancouver": "Canucks",
    # Vegas
    "VGK": "Golden Knights",
    "Vegas": "Golden Knights",
    "GoldenKnights": "Golden Knights",
    # Washington
    "WSH": "Capitals",
    "Washington": "Capitals",
    # Winnipeg
    "WPG": "Jets",
    "Winnipeg": "Jets",
}


NBA_KALSHI_BASE_URL = (
    "https://kalshi.com/markets/kxnbagame/professional-basketball-game/"
)

NHL_KALSHI_BASE_URL = "https://kalshi.com/markets/kxnhlgame/nhl-game/"


NFL_TEAM_MAPPING = {
    # Arizona
    "ARI": "Cardinals",
    "Arizona": "Cardinals",
    # Atlanta
    "ATL": "Falcons",
    "Atlanta": "Falcons",
    # Baltimore
    "BAL": "Ravens",
    "Baltimore": "Ravens",
    # Buffalo
    "BUF": "Bills",
    "Buffalo": "Bills",
    # Carolina
    "CAR": "Panthers",
    "Carolina": "Panthers",
    # Chicago
    "CHI": "Bears",
    "Chicago": "Bears",
    # Cincinnati
    "CIN": "Bengals",
    "Cincinnati": "Bengals",
    # Cleveland
    "CLE": "Browns",
    "Cleveland": "Browns",
    # Dallas
    "DAL": "Cowboys",
    "Dallas": "Cowboys",
    # Denver
    "DEN": "Broncos",
    "Denver": "Broncos",
    # Detroit
    "DET": "Lions",
    "Detroit": "Lions",
    # Green Bay
    "GB": "Packers",
    "Green Bay": "Packers",
    "GreenBay": "Packers",
    # Houston
    "HOU": "Texans",
    "Houston": "Texans",
    # Indianapolis
    "IND": "Colts",
    "Indianapolis": "Colts",
    # Jacksonville
    "JAX": "Jaguars",
    "Jacksonville": "Jaguars",
    # Kansas City
    "KC": "Chiefs",
    "Kansas City": "Chiefs",
    "KansasCity": "Chiefs",
    # Las Vegas
    "LV": "Raiders",
    "Las Vegas": "Raiders",
    "LasVegas": "Raiders",
    "OAK": "Raiders",  # Legacy abbreviation
    "Oakland": "Raiders",  # Legacy name
    # Los Angeles Chargers
    "LAC": "Chargers",
    "Los Angeles C": "Chargers",
    "Los Angeles Chargers": "Chargers",
    # Los Angeles Rams
    "LAR": "Rams",
    "LA": "Rams",
    "Los Angeles R": "Rams",
    "Los Angeles Rams": "Rams",
    # Miami
    "MIA": "Dolphins",
    "Miami": "Dolphins",
    # Minnesota
    "MIN": "Vikings",
    "Minnesota": "Vikings",
    # New England
    "NE": "Patriots",
    "New England": "Patriots",
    "NewEngland": "Patriots",
    # New Orleans
    "NO": "Saints",
    "New Orleans": "Saints",
    "NewOrleans": "Saints",
    # New York Giants
    "NYG": "Giants",
    "New York G": "Giants",
    # New York Jets
    "NYJ": "Jets",
    "New York J": "Jets",
    # Philadelphia
    "PHI": "Eagles",
    "Philadelphia": "Eagles",
    # Pittsburgh
    "PIT": "Steelers",
    "Pittsburgh": "Steelers",
    # San Francisco
    "SF": "49ers",
    "San Francisco": "49ers",
    "SanFrancisco": "49ers",
    # Seattle
    "SEA": "Seahawks",
    "Seattle": "Seahawks",
    # Tampa Bay
    "TB": "Buccaneers",
    "Tampa Bay": "Buccaneers",
    "TampaBay": "Buccaneers",
    "Tampa": "Buccaneers",
    # Tennessee
    "TEN": "Titans",
    "Tennessee": "Titans",
    # Washington
    "WAS": "Commanders",
    "Washington": "Commanders",
    "WSH": "Commanders",  # Alternative abbreviation
}


NFL_KALSHI_BASE_URL = "https://kalshi.com/markets/kxnflgame/professional-football-game/"
