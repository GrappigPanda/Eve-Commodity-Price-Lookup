import requests
import xml.etree.cElementTree as ET


class PlayerStats(dict):
    """
    Class operating as a container for player statistics, such as: corporation
    standing, accounting skill level, &c.
    """
    def __init__(self, keyid, vCode):
        self.key_id = keyid
        self.vCode = vCode
        self.standings = self.player_standings_lookup()
        self.acctng, self.relations = self.player_skill_lookup()

    def player_skill_lookup(self):
        results = []
        url_base = "https://api.eveonline.com/"
        char_param = "char/CharacterSheet.xml.aspx?keyID={}" \
                     "&vCode={}".format(self.key_id, self.vCode)
        typeIDs = [16622, 3446]  # Accounting then Broker Relations

        for id in typeIDs:
            url = url_base + char_param
            r = requests.get(url)
            root = ET.fromstring(r.text)
            x = root.findall('result/rowset[@name="skills"]/row[@typeID="3446"]')
            results.append(int(x[0].attrib['level']))

        return results[0], results[1]

    def player_standings_lookup(self):
        standings = {}

        url_base = "https://api.eveonline.com/"
        stand_param = "char/Standings.xml.aspx?keyID={}" \
                      "&vCode={}".format(self.key_id, self.vCode)

        url = url_base + stand_param
        r = requests.get(url)
        root = ET.fromstring(r.text)
        x = root.findall('result/characterNPCStandings/rowset[@name="NPCCorporations"]/row')
        y = root.findall('result/characterNPCStandings/rowset[@name="factions"]/row')
        
        for i in xrange(len(x)):
            standings[x[i].attrib['fromID']] = float(x[i].attrib['standing'])
            standings[y[i].attrib['fromID']] = float(y[i].attrib['standing'])

        return standings

    def key_lookup(self, key, i):
        common_values = {'Jita': ['1000035', '500001'],
                         'Amarr': ['1000086', '0']}
        try:
            return common_values[key][i]
        except KeyError:
            return None

if __name__ == "__main__":
    a = PlayerStats(111, "1111")
    print a.fact_stand
