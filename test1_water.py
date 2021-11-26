from opentrons import protocol_api

metadata = {'apiLevel': '2.10'}

def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('unchained_2x4_20ml', 2)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_1])

    #p300.transfer(100, plate['A1'], plate['B2'])
    p300.default_speed = 1200
    p300.distribute([100,100,100,100],plate['A1'],[plate['A2'],plate['A3'],plate['B2'],plate['B3']],blow_out = True,blowout_location = "source well", touch_tip = True, trash = False)
