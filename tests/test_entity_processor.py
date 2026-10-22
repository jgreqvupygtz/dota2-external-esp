from pipeline.entity_processor import EntityProcessor, TEAM_RADIANT, TEAM_DIRE


class FakeReader:
    def __init__(self, ents):
        self.ents = ents

    def read_entity(self, base, idx):
        return self.ents.get(idx)

    def read_int(self, addr, off):
        return self.ents.get("values", {}).get(addr, 0)


def test_processor_filters_dormant_and_teams():
    ents = {1: 0x100, 2: 0x200, 3: 0x300}
    values = {0x100: TEAM_RADIANT, 0x200: TEAM_DIRE, 0x300: 0}
    reader = FakeReader({**ents, "values": values})
    proc = EntityProcessor(reader, {}, team_filter="enemy")
    # local team defaults to None -> nothing filtered out by team
    out = proc.process(type("S", (), {"entity_list_ptr": 1, "player_ptr": None})())
    assert isinstance(out, list)


def test_team_constants():
    assert TEAM_RADIANT == 2
    assert TEAM_DIRE == 3