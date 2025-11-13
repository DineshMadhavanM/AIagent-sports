import re
from typing import Optional

SPORT_KEYWORDS = {
    "cricket": ["cricket", "odi", "test", "t20", "ipl", "runs", "wickets"],
    "football": ["football", "soccer", "goal", "premier league", "la liga", "world cup"],
    "basketball": ["basketball", "nba", "points", "rebounds", "assists", "three-pointer"],
    "tennis": ["tennis", "grand slam", "set", "game", "ace", "break"],
}


def infer_sport(text: str) -> Optional[str]:
    t = text.lower()
    for sport, keys in SPORT_KEYWORDS.items():
        if any(k in t for k in keys):
            return sport
    return None


def is_rules_query(t: str) -> bool:
    t = t.lower()
    return any(k in t for k in ["rules", "how to play", "format", "formats", "scoring", "points system"]) \
        or bool(re.search(r"how\s+does\s+.*\s+work", t))


def is_summary_query(t: str) -> bool:
    t = t.lower()
    return any(k in t for k in ["summary", "recap", "what happened", "match report", "breakdown"]) \
        or ("vs" in t or "v." in t)


def is_stats_query(t: str) -> bool:
    t = t.lower()
    return any(k in t for k in ["stats", "statistics", "numbers", "record", "averages", "efficiency"]) \
        or ("compare" in t and "player" in t)


def is_commentary_query(t: str) -> bool:
    t = t.lower()
    return any(k in t for k in ["commentary", "play-by-play", "live text", "radio style"]) \
        or ("call the" in t and "play" in t)


def is_news_or_prediction(t: str) -> bool:
    t = t.lower()
    return any(k in t for k in ["news", "headline", "brief", "prediction", "preview", "outlook"]) \
        or ("who will win" in t)


class RuleBasedProvider:
    def generate(self, query: str) -> str:
        sport = infer_sport(query)
        q = query.strip()

        if is_rules_query(q):
            return self._rules_response(sport)
        if is_summary_query(q):
            return self._summary_response(sport)
        if is_stats_query(q):
            return self._stats_response(sport)
        if is_commentary_query(q):
            return self._commentary_response(sport)
        if is_news_or_prediction(q):
            return self._news_or_prediction_response(sport)
        return self._general_response(sport)

    def _rules_response(self, sport: Optional[str]) -> str:
        if sport == "cricket":
            return (
                "Cricket basics\n"
                "- Format: Tests (5 days), ODIs (50 overs/side), T20s (20 overs/side).\n"
                "- Objective: Batting side scores runs; bowling side takes wickets or limits runs.\n"
                "- Scoring: 1–3 runs by running; 4 for boundary along ground; 6 for clearing the rope; extras include wides/no-balls.\n"
                "- Dismissals: Bowled, caught, lbw, run-out, stumped, hit-wicket.\n"
                "- Result: Higher total wins; ties and draws possible depending on format."
            )
        if sport == "football":
            return (
                "Football (soccer) basics\n"
                "- Duration: 90 minutes plus stoppage.\n"
                "- Objective: Score more goals than the opponent.\n"
                "- Scoring: Entire ball crosses goal line between posts and under bar.\n"
                "- Key rules: Offside, fouls/misconduct, free-kicks, penalties.\n"
                "- Competitions: Leagues (round-robin) and cups (knockout)."
            )
        if sport == "basketball":
            return (
                "Basketball basics\n"
                "- Duration: 4 quarters (NBA: 12 min each).\n"
                "- Scoring: 2 points inside arc, 3 points beyond, 1 for free throws.\n"
                "- Violations: Traveling, double-dribble, shot-clock, backcourt.\n"
                "- Fouls: Personal, team foul limit leads to free throws.\n"
                "- Overtime: If tied, 5-minute periods until a winner."
            )
        if sport == "tennis":
            return (
                "Tennis basics\n"
                "- Structure: Points → games → sets → match.\n"
                "- Scoring: 0–15–30–40–game (two-point lead at deuce).\n"
                "- Tie-breaks: First to 7 (win by 2) for sets; formats vary by event.\n"
                "- Surfaces: Hard, clay, grass influence bounce and style.\n"
                "- Faults: Double-fault loses point; let on serve is replayed."
            )
        return (
            "General sports scoring and formats\n"
            "- Objective: Outscore the opponent within the rules and time/overs/sets.\n"
            "- Formats: League (round-robin), knockout, series, tournaments.\n"
            "- Scoring: Points/goals/runs depending on sport; penalties for infractions.\n"
            "- Officials: Enforce rules; video review in many modern competitions."
        )

    def _summary_response(self, sport: Optional[str]) -> str:
        if sport == "cricket":
            return (
                "Match summary template (cricket)\n"
                "- Teams: Team A vs Team B\n"
                "- Toss/Decision: Team A won toss and chose to bat/bowl\n"
                "- Scorecards: A: 000/0 (ov) | B: 000/0 (ov)\n"
                "- Key performers: Top-scorer, best bowler, turning spell\n"
                "- Turning moments: Partnership, powerplay, death overs\n"
                "- Result: Winner by margin; Player of the Match\n"
                "Provide teams, format, and notable events for a tailored recap."
            )
        if sport == "football":
            return (
                "Match summary template (football)\n"
                "- Scoreline: Team A 0–0 Team B\n"
                "- Timeline: Goals, key chances, VAR decisions\n"
                "- Tactics: Formations, pressing, transitions\n"
                "- Standouts: Best attacker, midfielder, defender, goalkeeper\n"
                "- X-factor: Substitutions, set-pieces, pressing traps\n"
                "Share teams, competition, and minute-by-minute highlights for detail."
            )
        if sport == "basketball":
            return (
                "Game summary template (basketball)\n"
                "- Final: Team A 00 – 00 Team B\n"
                "- Runs: 10–0 swing, third-quarter surge\n"
                "- Efficiency: eFG%, ORB%, turnover battle\n"
                "- Matchups: Star vs primary defender, bench impact\n"
                "- Clutch: Last 2 minutes shot chart and decisions\n"
                "Provide teams, league, and key runs for a tailored recap."
            )
        if sport == "tennis":
            return (
                "Match summary template (tennis)\n"
                "- Score: 7–6, 3–6, 6–4\n"
                "- Patterns: Serve +1 plays, rally length, backhand exchanges\n"
                "- Momentum: Early breaks, mid-set resets, tie-breaks\n"
                "- Adjustments: Return position, spin/pace mix, net approaches\n"
                "- Finish: Closing patterns and nerves\n"
                "Share players, surface, and set scores for specificity."
            )
        return (
            "Generic match summary template\n"
            "- Final score/result\n"
            "- Key momentum swings\n"
            "- Tactical themes\n"
            "- Standout performers\n"
            "- Critical decisions or officiating moments\n"
            "Add teams/players and context for a tailored report."
        )

    def _stats_response(self, sport: Optional[str]) -> str:
        if sport == "basketball":
            return (
                "Basketball stats guide\n"
                "- Box: PTS, REB, AST, STL, BLK, TOV, FG%, 3P%, FT%.\n"
                "- Advanced: TS%, eFG%, USG%, ORtg/DRtg, BPM.\n"
                "- Context: Pace, role, opponent quality.\n"
                "Share players/season to compare and I’ll analyze the profiles."
            )
        if sport == "football":
            return (
                "Football stats guide\n"
                "- Attacking: xG, xA, key passes, progressive carries.\n"
                "- Defensive: Tackles, interceptions, pressures, aerials.\n"
                "- Team: PPDA, field tilt, set-piece xG.\n"
                "Provide players/teams and competition for a sharper read."
            )
        if sport == "cricket":
            return (
                "Cricket stats guide\n"
                "- Batting: Avg, SR, 50/100, boundary %, dot-ball %.\n"
                "- Bowling: Economy, Avg, SR, dot-ball %, phase splits.\n"
                "- Fielding: Catches, run-outs.\n"
                "Give player names, format, and span for analysis."
            )
        if sport == "tennis":
            return (
                "Tennis stats guide\n"
                "- Serve: Ace%, 1st serve in/won, 2nd serve won.\n"
                "- Return: 1st/2nd return points won, break conversion.\n"
                "- Rally: Winners, UEs, rally length distribution.\n"
                "Share players/surface/event to contextualize."
            )
        return (
            "General stats guide\n"
            "- Identify core metrics, add advanced context, compare roles/opponents.\n"
            "Share specific names and timeframe for a focused breakdown."
        )

    def _commentary_response(self, sport: Optional[str]) -> str:
        if sport == "football":
            return (
                "Commentary (sample)\n"
                "Kick-off. The press is aggressive from the visitors. Minute 12: a clipped pass splits the line; the winger drives inside—low cross—palmed away. Minute 37: corner swung in, near-post flick, off the bar. Second half, 71: substitute injects pace, one-two at the edge, curled finish into the far corner. The stadium erupts."
            )
        if sport == "basketball":
            return (
                "Commentary (sample)\n"
                "Opening tip secured. Early pick-and-roll, pocket pass—two hands for safety. A 9–2 burst forces a timeout. Third quarter: star drills back-to-back threes from the logo. Final minute: switch-hunt, step-back at the horn—got it."
            )
        if sport == "cricket":
            return (
                "Commentary (sample)\n"
                "Over begins. Good length on off; defended. Shorter next—pulled behind square for four. Changes the angle, slanting across—edge! Flying slip just wide. The field creeps in; slower ball deceives, lofted—safe on the bounce."
            )
        if sport == "tennis":
            return (
                "Commentary (sample)\n"
                "New balls. Kicks to the backhand, shoulder-high reply. Inside-out forehand opens the court; approach and soft hands at net—holds serve. Break point next game: heavy return pins the server, backhand down the line—break secured."
            )
        return (
            "Commentary (sample)\n"
            "Tense opening, momentum swings through the middle phase, decisive play in the closing moments."
        )

    def _news_or_prediction_response(self, sport: Optional[str]) -> str:
        base = (
            "News brief / outlook\n"
            "- This is a hypothetical brief based on typical trends, not real-time data.\n"
        )
        if sport == "football":
            return base + (
                "- Themes: Mid-block vs high press, set-piece edge, transition threats.\n"
                "- Outlook: If Team A controls midfield tempo and limits turnovers, they tilt the odds."
            )
        if sport == "basketball":
            return base + (
                "- Themes: Three-point volume, rim attempts, defensive rebounding.\n"
                "- Outlook: Team with better shot quality and turnover margin projects ahead."
            )
        if sport == "cricket":
            return base + (
                "- Themes: Powerplay strike rate, middle-overs control, death-overs execution.\n"
                "- Outlook: Conditions and match-ups (pace vs spin) likely decide it."
            )
        if sport == "tennis":
            return base + (
                "- Themes: Serve dominance, rally tolerance, backhand stability.\n"
                "- Outlook: Surface-speed and return depth shape the matchup."
            )
        return base + (
            "- Themes: Efficiency, turnovers, set-piece/special-teams moments.\n"
            "- Outlook: Execute fundamentals, exploit mismatches, manage game states."
        )

    def _general_response(self, sport: Optional[str]) -> str:
        if sport:
            return (
                f"What would you like to know about {sport}? Specify rules, summaries, stats, commentary, news/outlook, or general knowledge."
            )
        return (
            "Which sport are you asking about? I can cover cricket, football, basketball, tennis, and more—rules, summaries, stats, commentary, news-style briefs, or predictions."
        )
