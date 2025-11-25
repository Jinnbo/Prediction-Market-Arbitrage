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


CFB_TEAM_MAPPING = {
    # Air Force
    "AFA": "AirForce",
    "AF": "AirForce",
    # Alabama
    "ALA": "Alabama",
    # Appalachian State
    "APP": "AppalachianState",
    # Arizona
    "ARIZ": "Arizona",
    # Arizona State
    "ASU": "ArizonaState",
    # Arkansas
    "ARK": "Arkansas",
    # Arkansas State
    "ARST": "ArkansasState",
    # Army
    "ARMY": "Army",
    # Auburn
    "AUB": "Auburn",
    # Ball State
    "BALL": "BallState",
    # Baylor
    "BAY": "Baylor",
    # Boise State
    "BSU": "BoiseState",
    # Boston College
    "BC": "BostonCollege",
    # Bowling Green
    "BGSU": "Bowling",
    # Buffalo
    "BUFF": "Buffalo",
    "BUF": "Buffalo",
    # BYU
    "BYU": "BYU",
    # California
    "CAL": "California",
    # Central Michigan
    "CMU": "CentralMichigan",
    # Charlotte
    "CHAR": "Charlotte49ers",
    # Cincinnati
    "CIN": "Cincinnati",
    # Clemson
    "CLEM": "Clemson",
    # Coastal Carolina
    "CCAR": "CoastalCarolinaChanticleers",
    "CCU": "CoastalCarolinaChanticleers",
    # Colorado
    "COLO": "Colorado",
    # Colorado State
    "CSU": "ColoradoState",
    # Delaware
    "DEL": "DelawareBlueHens",
    # Duke
    "DUKE": "Duke",
    # East Carolina
    "ECU": "EastCarolina",
    # Eastern Michigan
    "EMU": "EasternMichigan",
    # Florida
    "FLA": "FloridaGators",
    "UF": "FloridaGators",
    # Florida Atlantic
    "FAU": "FloridaAtlantic",
    # Florida International
    "FIU": "FloridaInternational",
    # Florida State
    "FSU": "FloridaState",
    # Fresno State
    "FRES": "FresnoState",
    # Georgia
    "UGA": "Georgia",
    # Georgia Southern
    "GASO": "GeorgiaSouthern",
    # Georgia State
    "GAST": "GeorgiaState",
    # Georgia Tech
    "GT": "GeorgiaTech",
    # Hawaii
    "HAW": "Hawaii",
    # Houston
    "HOU": "Houston",
    # Illinois
    "ILL": "Illinois",
    # Indiana
    "IND": "Indiana",
    # Iowa
    "IOWA": "Iowa",
    # Iowa State
    "ISU": "IowaState",
    # James Madison
    "JMU": "JamesMadison",
    # Jacksonville State
    "JVST": "JacksonvilleState",
    # Kansas
    "KU": "Kansas",
    # Kansas State
    "KSU": "KansasState",
    # Kent State
    "KENT": "KentStateGoldenFlashes",
    # Kennesaw State
    "KENN": "KennesawState",
    # Kentucky
    "UK": "Kentucky",
    # Liberty
    "LIB": "Liberty",
    # Louisiana
    "ULL": "Louisiana",
    "UL": "Louisiana",
    # Louisiana Monroe
    "ULM": "ULMonroe",
    # Louisiana Tech
    "LT": "LouisianaTech",
    "LATECH": "LouisianaTech",
    # Louisville
    "LOU": "Louisville",
    # LSU
    "LSU": "LSU",
    # Marshall
    "MRSH": "Marshall",
    # Maryland
    "MD": "MarylandTerrapins",
    # Memphis
    "MEM": "Memphis",
    # Miami (FL)
    "MIA": "Miami",
    # Miami (OH)
    "M-OH": "Miami(OH)",
    "MOH": "Miami(OH)",
    # Michigan
    "MICH": "Michigan",
    # Michigan State
    "MSU": "MichiganState",
    # Middle Tennessee
    "MTU": "MiddleTennessee",
    "MTSU": "MiddleTennessee",
    # Minnesota
    "MINN": "Minnesota",
    # Mississippi State
    "MSST": "MississippiState",
    # Missouri
    "MIZZ": "Missouri",
    "MIZ": "Missouri",
    # Missouri State
    "MOSU": "MissouriState",
    # Navy
    "NAVY": "Navy",
    # NC State
    "NCST": "NCState",
    # Nebraska
    "NEB": "NebraskaCornhuskers",
    # Nevada
    "NEV": "NevadaWolfPack",
    # New Mexico
    "UNM": "NewMexico",
    # New Mexico State
    "NMSU": "NewMexicoState",
    # North Carolina
    "UNC": "NorthCarolina",
    # North Texas
    "UNT": "NorthTexas",
    # Northern Illinois
    "NIU": "NorthernIllinois",
    # Northwestern
    "NW": "Northwestern",
    # Notre Dame
    "ND": "NotreDame",
    # Ohio
    "OHIO": "Ohio",
    # Ohio State
    "OSU": "OhioState",
    # Oklahoma
    "OKLA": "Oklahoma",
    "OU": "Oklahoma",
    # Oklahoma State
    "OKST": "OklahomaState",
    # Old Dominion
    "ODU": "OldDominion",
    # Ole Miss
    "MISS": "OleMiss",
    # Oregon
    "ORE": "Oregon",
    # Oregon State
    "ORST": "OregonState",
    # Penn State
    "PSU": "PennState",
    # Pittsburgh
    "PITT": "Pittsburgh",
    # Purdue
    "PUR": "PurdueBoilermakers",
    # Rice
    "RICE": "Rice",
    # Rutgers
    "RUTG": "Rutgers",
    # Sam Houston
    "SHSU": "SamHoustonBearkats",
    # San Diego State
    "SDSU": "SanDiegoState",
    # San Jose State
    "SJSU": "SanJoseState",
    # SMU
    "SMU": "SMUMustangs",
    # South Alabama
    "USA": "SouthAlabama",
    # South Carolina
    "SCAR": "SouthCarolina",
    # South Florida
    "USF": "SouthFlorida",
    # Southern Miss
    "USM": "SouthernMiss",
    # Stanford
    "STAN": "Stanford",
    # Syracuse
    "SYR": "Syracuse",
    # TCU
    "TCU": "TCU",
    # Temple
    "TEM": "Temple",
    # Tennessee
    "TENN": "Tennessee",
    # Texas
    "TEX": "Texas",
    "UT": "Texas",
    # Texas A&M
    "TXAM": "TexasA&M",
    "TAMU": "TexasA&M",
    # Texas State
    "TXST": "TexasState",
    # Texas Tech
    "TTU": "TexasTechRedRaiders",
    # Toledo
    "TOL": "Toledo",
    # Troy
    "TROY": "Troy",
    # Tulane
    "TULN": "Tulane",
    # Tulsa
    "TLSA": "Tulsa",
    # UAB
    "UAB": "UABBlazers",
    # UCF
    "UCF": "UCF",
    # UCLA
    "UCLA": "UCLA",
    # UMass
    "MASS": "UMass",
    "UMASS": "UMass",
    # UNLV
    "UNLV": "UNLV",
    # USC
    "USC": "USC",
    # Utah
    "UTAH": "Utah",
    # Utah State
    "USU": "UtahState",
    # UTEP
    "UTEP": "UTEP",
    # UTSA
    "UTSA": "UTSARoadrunners",
    # Vanderbilt
    "VAN": "Vanderbilt",
    "VANDY": "Vanderbilt",
    # Virginia
    "UVA": "Virginia",
    # Virginia Tech
    "VT": "VirginiaTech",
    # Wake Forest
    "WAKE": "WakeForest",
    # Washington
    "WASH": "Washington",
    # Washington State
    "WSU": "WashingtonState",
    # West Virginia
    "WVU": "WestVirginia",
    # Western Kentucky
    "WKU": "WesternKentucky",
    # Western Michigan
    "WMU": "WesternMichigan",
    # Wisconsin
    "WIS": "WisconsinBadgers",
    # Wyoming
    "WYO": "Wyoming",
}


CFB_KALSHI_BASE_URL = "https://kalshi.com/markets/kxncaafgame/college-football-game/"
