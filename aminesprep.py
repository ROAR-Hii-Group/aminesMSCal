from numpy import array
from opentrons import protocol_api

metadata = {'apiLevel': '2.10'}

def run(protocol: protocol_api.ProtocolContext):
    #directPerc = [100,95,70,50]
    #tmpStockPerc = 25
    #numberDilutionSeries = 7
    tarVol = 500

    compounds = {
        "A11":"A1",
        "A12":"A2",
        "A13":"A3",
        "A14":"A4",
        "A15":"B1",
        "A16":"B2",
        "A17":"B3",
        "A18":"B4"
        }

    solventPlate= protocol.load_labware('roarprinted_2_reservoir_125000_shallow', 3)
    solventVial = solventPlate['A1']
    stockPlate = protocol.load_labware('unchained_2x4_20ml', 5)
    tiprack_1000 = protocol.load_labware('opentrons_96_tiprack_1000ul', 8)
    tiprack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 7)
    multipip = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_300])
    singpip = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[tiprack_1000])
    samplePlate = protocol.load_labware('porvairpp_96_wellplate_2000ul',2)

    singpip.default_speed = 1200
    multipip.default_speed = 1200

    #from stock
    compound_list = compounds.keys()
    samplerow = 0
    for i in compound_list:
        stockVial = stockPlate[compounds[i]]
        singpip.distribute(tarVol*2/10, stockVial, samplePlate.columns()[0][samplerow], blow_out = True, touch_tip = False, blowout_location = "source well", rate = 2)
        #singpip.distribute(list(array((directPerc + [tmpStockPerc*2]))/100*tarVol), stockVial, rowlist[:len(directPerc)+1],touch_tip = False, blowout_location = "source well", rate = 2)
        samplerow += 1

    #solvent
    #singpip.distribute((list((100-array(directPerc))/100*tarVol)+[(100-tmpStockPerc)/100*tarVol*2]+[tarVol]*numberDilutionSeries)*len(compound_list), solventVial, [x.top(-1) for it in samplePlate.rows()[:len(compounds)] for x in it],touch_tip = False, blowout_location = "source well",rate = 2)
    singpip.distribute([tarVol*2/10*9,tarVol*2/10*9,tarVol,tarVol,tarVol,tarVol,tarVol,tarVol,tarVol,tarVol,tarVol,tarVol]*8, solventVial, [x.top(-1) for it in samplePlate.rows()[:len(compounds)] for x in it], blowout_location = "source well", blow_out = True, touch_tip = False, rate = 2)



    #series
    multipip.pick_up_tip()

    multipip.transfer(tarVol*2/10, samplePlate.rows()[0][0],samplePlate.rows()[0][1], new_tip = "never", blow_out = False, touch_tip = False, mix_after = (3, tarVol/2))
    multipip.transfer(tarVol*2/10, samplePlate.rows()[0][1],samplePlate.rows()[0][2], new_tip = "never", blow_out = False, touch_tip = False, mix_after = (3, tarVol/2))


    for i in range(2,12):
        multipip.transfer(tarVol, samplePlate.rows()[0][i],samplePlate.rows()[0][i+1], new_tip = "never", blow_out = False, touch_tip = False, mix_after = (3, tarVol/2))
        
    multipip.drop_tip()
