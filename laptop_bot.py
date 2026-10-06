import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "8865466492:AAGK5IFtq-_P2YShJxSEn5TA-i2mVh29G4o")
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "4152ff242fe7df21348b217b5bd0ec8f")

TOP_5 = {
    "soccer_epl": "Premier League",
    "soccer_spain_la_liga": "La Liga",
    "soccer_germany_bundesliga": "Bundesliga",
    "soccer_italy_serie_a": "Serie A",
    "soccer_france_ligue_one": "Ligue 1"
}

def get_best_odds_for_league(sport_key):
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    params = {"apiKey": ODDS_API_KEY, "regions": "eu,uk", "markets": "h2h", "oddsFormat": "decimal"}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error {sport_key}: {e}")
        return []

def analyze_match(match):
    home = match['home_team']
    away = match['away_team']
    sport_key = match.get('sport_key','')
    best = {"home": (0, ""), "draw": (0, ""), "away": (0, "")}
    for bm in match.get('bookmakers', []):
        for market in bm.get('markets', []):
            if market['key']!= 'h2h': continue
            for o in market['outcomes']:
                name, price = o['name'], o['price']
                if name == home and price > best["home"][0]: best["home"] = (price, bm['title'])
                elif name == away and price > best["away"][0]: best["away"] = (price, bm['title'])
                elif price > best["draw"][0]: best["draw"] = (price, bm['title'])
    if best["home"][0] == 0: return None
    p_home = 1 / best["home"][0]
    p_draw = 1 / best["draw"][0]
    p_away = 1 / best["away"][0]
    total = p_home + p_draw + p_away
    prob_home = round((p_home/total)*100,1)
    prob_draw = round((p_draw/total)*100,1)
    prob_away = round((p_away/total)*100,1)
    max_prob = max(prob_home, prob_draw, prob_away)
    if prob_home == max_prob:
        pred = f"HOME WIN ({home}) - {prob_home}%"
        best_bet = f"1 @ {best['home'][0]} ({best['home'][1]})"
    elif prob_away == max_prob:
        pred = f"AWAY WIN ({away}) - {prob_away}%"
        best_bet = f"2 @ {best['away'][0]} ({best['away'][1]})"
    else:
        pred = f"DRAW - {prob_draw}%"
        best_bet = f"X @ {best['draw'][0]} ({best['draw'][1]})"
    league = TOP_5.get(sport_key, sport_key)
    return f"⚽ {home} vs {away}\n🏆 {league}\n\n📊 PREDICTION:\n{pred}\n\n💰 BEST ODDS:\n1: {best['home'][0]} @ {best['home'][1]} ({prob_home}%)\nX: {best['draw'][0]} @ {best['draw'][1]} ({prob_draw}%)\n2: {best['away'][0]} @ {best['away'][1]} ({prob_away}%)\n\n🎯 BEST BET: {best_bet}\n"

async def top5_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Scanning Top 5 Leagues - Best Odds + Prediction...")
    all_text=""; count=0
    for key,name in TOP_5.items():
        games=get_best_odds_for_league(key)
        if not games: continue
        all_text+=f"\n=== {name.upper()} ===\n"
        for g in games[:5]:
            f=analyze_match(g)
            if f: all_text+=f+"\n"; count+=1
    if count==0: all_text="No games or API limit. Try later."
    for i in range(0,len(all_text),4000):
        await update.message.reply_text(all_text[i:i+4000])

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.message.text.lower()
    for key in TOP_5:
        for g in get_best_odds_for_league(key):
            txt=f"{g['home_team']} vs {g['away_team']}".lower()
            if q.replace('vs','').strip() in txt or q in txt:
                f=analyze_match(g)
                if f: await update.message.reply_text(f); return
    await update.message.reply_text("Not found in Top 5. Use /top5")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ BOT V3 LIVE - Best Odds + Prediction\n\n/top5 - Top 5 leagues\nType team name")

def main():
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("top5",top5_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))
    print("BOT @muta_748_bot RUNNING - V3 Best Odds + Prediction...")
    app.run_polling()

if __name__=="__main__":
    main()
