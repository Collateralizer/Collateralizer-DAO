import pytest
from brownie import *
import typer
import json


@pytest.fixture(scope="module", autouse=True)
def deployedContracts():

    deployed = open("config.json", "r")

    try:
        deployed = json.loads(deployed.read())
    except:
        deployed = {}

    ENV = ""
    if (network.chain.id == 1):
        ENV = "prod"
    else:
        ENV = "dev"

    # list of 10 use-n-throw addresses
    addresses = ['0x4ce799e6eD8D64536b67dD428565d52A531B3640', '0x4e14672D1Ed1FEFAc9948456006a4015D186C15E', '0x6EDfA9fb275f389a641c8C3c85DdF29dF2Ca8EC7', '0x57813f12d90177bE50ec25Fb60bd2BaC1558fd9C', '0xF65fA4C233CDA7aA7a3563d824809231b138cf11',
                 '0x10Cdd8CDaa3c402AA2fc3d6a29b6D79424f77fDB', '0x8E60704Fa16bE888a0EcBFD68DF34DfC9D066A15', '0x6FE46dd39f8289218f99448DEdAFa2fD4C483aDc', '0x0D935F1Da128b34698Dc3274a9F39bAF2D6C79eE', '0x02a22054d42C50797dcBFeE3077C767b2c9864EB']

    # account used for executing transactions
    DEFAULT_DEPLOYER_ACCOUNT = accounts.at(addresses[0], force=True)
    # DEFAULT_DEPLOYER_ACCOUNT = accounts.load('stakedao-deployer-rug-pull')
    deployer = {'from': DEFAULT_DEPLOYER_ACCOUNT}

    # Existing GnosisSafe mainnet address
    GNOSISSAFE_MASTERCOPY = '0x34CfAC646f301356fAa8B21e94227e3583Fe3F5F'

    # Existing GnosisSafeProxyFactory mainnet address
    GNOSISSAFE_PROXY_FACTORY = '0x76E2cFc1F5Fa8F6a5b3fC4c8F4788F0116861F9B'

    GNOSIS_SAFE_PROXY = deployed[ENV]['GNOSIS_SAFE_PROXY']
    multisig = {'from': GNOSIS_SAFE_PROXY}

    # Curve TokenMinter mainnet address
    TOKEN_MINTER = '0xd061D61a4d941c39E5453435B6345Dc261C2fcE0'

    # YEARN_DEPLOYER = accounts.at(addresses[1], force=True)

    # an array of 3 owners of governance multisig
    GOVERNANCE_OWNERS = []
    for i in range(2, 5):
        GOVERNANCE_OWNERS.append(accounts.at(addresses[i], force=True))

    # Strategist account
    STRATEGIST = accounts.at(addresses[5], force=True)

    # trx data for setting up owners and threshold for governance multisig
    DATA = "0xb63e800d0000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030000000000000000000000004e14672d1ed1fefac9948456006a4015d186c15e0000000000000000000000006edfa9fb275f389a641c8c3c85ddf29df2ca8ec700000000000000000000000057813f12d90177be50ec25fb60bd2bac1558fd9c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000"

    # DAI mainnet token address
    DAI = '0x6B175474E89094C44Da98b954EedeAC495271d0F'

    # sbtcCrv Token mainnet address
    SBTC_CRV = '0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3'

    # 3Crv Token mainnet address
    THREE_CRV = '0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490'

    # eursCrv Token mainnet address
    EURS_CRV = '0x194eBd173F6cDacE046C53eACcE9B953F28411d1'

    # Keepr address
    Keep3r = '0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44'

    STRATEGY_PROXY = deployed[ENV]['STRATEGY_PROXY']
    # Deploy StrategyProxy
    strategyProxy = StrategyProxy.at(STRATEGY_PROXY)

    strategyCurveEursCrvVoterProxy = StrategyCurveEursCrvVoterProxy.at(
        deployed[ENV]['STRATEGY_CURVE_EURS_CRV_VOTER_PROXY'])

    strategyCurveBTCVoterProxy = StrategyCurveBTCVoterProxy.at(
        deployed[ENV]['STRATEGY_CURVE_BTC_VOTER_PROXY'])

    strategyCurve3CrvVoterProxy = StrategyCurve3CrvVoterProxy.at(
        deployed[ENV]['STRATEGY_CURVE_3CRV_VOTER_PROXY'])

    # 3Crv minter
    THREE_CRV_MINTER = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'
    curve3Pool = Contract(THREE_CRV_MINTER)

    # sbtc minter
    SBTC_CRV_MINTER = '0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714'

    # eursCrv minter
    EURS_CRV_MINTER = '0x0Ce6a5fF5217e38315f87032CF90686C96627CAA'

    # DAI bags
    DAI_HOLDER = '0x70178102AA04C5f0E54315aA958601eC9B7a4E08'

    # Curve Voting Escrow
    VOTING_ESCROW = '0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2'
    votingEscrow = Contract(VOTING_ESCROW)

    FEE_DISTRI = '0xA464e6DCda8AC41e03616F95f4BC98a13b8922Dc'
    feeDistri = Contract(FEE_DISTRI)

    # number of SDT minted per block at the time of deployment
    SDT_PER_BLOCK = 1000

    sender = {'from': DEFAULT_DEPLOYER_ACCOUNT}

    CRV_HOLDER = '0x4ce799e6eD8D64536b67dD428565d52A531B3640'

    crv = CRV.at('0xD533a949740bb3306d119CC777fa900bA034cd52')

    crvBal = crv.balanceOf(CRV_HOLDER)

    crv.transfer(DEFAULT_DEPLOYER_ACCOUNT, crvBal, {'from': CRV_HOLDER})

    dai = VaultToken.at(DAI)

    daiBal = dai.balanceOf(DAI_HOLDER)

    dai.transfer(DEFAULT_DEPLOYER_ACCOUNT, daiBal, {'from': DAI_HOLDER})

    # CurveYCRVVoter mainnet address
    CURVE_YCRV_VOTER = deployed[ENV]['CURVE_YCRV_VOTER']
    # CURVE_YCRV_VOTER = '0xF147b8125d2ef93FB6965Db97D6746952a133934'
    curveYCRVVoter = CurveYCRVVoter.at(CURVE_YCRV_VOTER)

    VE_CURVE_VAULT = deployed[ENV]['VE_CURVE_VAULT']
    # VE_CURVE_VAULT = '0xc5bDdf9843308380375a611c18B50Fb9341f502A'
    veCurve = veCurveVault.at(VE_CURVE_VAULT)

    sbtcCrv = VaultToken.at(SBTC_CRV)
    threeCrv = VaultToken.at(THREE_CRV)
    eursCrv = VaultToken.at(EURS_CRV)

    EURS_CRV_VAULT = deployed[ENV]['EURS_CRV_VAULT']
    # THREE_POOL_VAULT
    THREE_POOL_VAULT = "0xB17640796e4c27a39AF51887aff3F8DC0daF9567"
    # SBTC_VAULT
    SBTC_VAULT = "0x24129B935AfF071c4f0554882C0D9573F4975fEd"

    eursCrvVault = yVault.at(EURS_CRV_VAULT)
    threePoolVault = yVault.at(THREE_POOL_VAULT)
    sbtcCrvVault = yVault.at(SBTC_VAULT)

    sbtcBal = 10000000000000000000000000000
    threeCrvBal = 10000000000000000000000000000
    eursCrvBal = 10000000000000000000000000000

    CONTROLLER = deployed[ENV]['CONTROLLER']
    controller = Controller.at(CONTROLLER)

    TREASURY_VAULT = deployed[ENV]['TREASURY_VAULT']
    treasuryVault = TreasuryVault.at(TREASURY_VAULT)

    EURS_CRV = deployed[ENV]['EURS_CRV']
    eursCrv = VaultToken.at(EURS_CRV)

    SNX = "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"
    EURS = "0xdB25f211AB05b1c97D595516F45794528a807ad8"
    snx = Contract(SNX)
    eurs = Contract(EURS)

    # threeCrv.mint(DEFAULT_DEPLOYER_ACCOUNT, threeCrvBal,
    #               {'from': THREE_CRV_MINTER})
    # eursCrv.mint(DEFAULT_DEPLOYER_ACCOUNT, eursCrvBal,
    #              {'from': EURS_CRV_MINTER})
    # sbtc.mint(DEFAULT_DEPLOYER_ACCOUNT, sbtcBal, {'from': SBTC_CRV_MINTER})

    # threeCrv.approve(threePoolVault.address, threeCrvBal, sender)
    # eursCrv.approve(eursCrvVault.address, eursCrvBal, sender)
    # sbtc.approve(sbtcVault.address, sbtcBal, sender)
    # MALICE = '0x55FE002aefF02F77364de339a1292923A15844B8'
    # PLEB = '0x0E33Be39B13c576ff48E14392fBf96b02F40Cd34'
    # PLEB = '0xD6216fC19DB775Df9774a6E33526131dA7D19a2c'
    PLEB = '0x6512cbdad4d76ff79d3e96ace168f2e1315c1ece'
    pleb = {'from': PLEB}

    # return {'threePoolVault': threePoolVault, 'eursCrvVault': eursCrvVault, 'sbtcVault': sbtcVault, 'sender': sender, 'DEFAULT_DEPLOYER_ACCOUNT': DEFAULT_DEPLOYER_ACCOUNT, 'eursCrv': eursCrv, 'threeCrv': threeCrv, 'sbtc': sbtc, 'strategyCurveEursCrvVoterProxy': strategyCurveEursCrvVoterProxy, 'strategyCurve3CrvVoterProxy': strategyCurve3CrvVoterProxy, 'strategyCurveBTCVoterProxy': strategyCurveBTCVoterProxy, 'veCurve': veCurve, 'crv': crv, 'crvBal': crvBal, 'threeCrvBal': threeCrvBal, 'eursCrvBal': eursCrvBal, 'sbtcBal': sbtcBal, 'veCurve': veCurve, 'STRATEGIST': STRATEGIST, 'controller': controller, 'governanceGSPAddress': governanceGSPAddress, 'daiBal': daiBal, 'dai': dai, 'sdtToken': sdtToken, 'masterchef': masterchef, 'timelockGovernance': timelockGovernance, 'treasuryVault': treasuryVault, 'governanceStaking': governanceStaking}
    return {'sender': sender, 'DEFAULT_DEPLOYER_ACCOUNT': DEFAULT_DEPLOYER_ACCOUNT,
            'crv': crv, 'crvBal': crvBal, 'veCurve': veCurve, 'votingEscrow': votingEscrow,
            'curveYCRVVoter': curveYCRVVoter, 'curve3Pool': curve3Pool, 'threeCrv': threeCrv,
            'feeDistri': feeDistri, 'pleb': pleb, 'STRATEGY_PROXY': STRATEGY_PROXY,
            'multisig': multisig, 'strategyProxy': strategyProxy, 'strategyCurveEursCrvVoterProxy': strategyCurveEursCrvVoterProxy,
            'strategyCurveBTCVoterProxy': strategyCurveBTCVoterProxy, 'strategyCurve3CrvVoterProxy': strategyCurve3CrvVoterProxy,
            'GNOSIS_SAFE_PROXY': GNOSIS_SAFE_PROXY, 'deployer': deployer, 'eursCrvVault': eursCrvVault,
            'threePoolVault': threePoolVault, 'sbtcCrvVault': sbtcCrvVault, 'controller': controller,
            'treasuryVault': treasuryVault, 'EURS_CRV': EURS_CRV, 'sbtcCrv': sbtcCrv, 'eursCrv': eursCrv,
            'snx': snx, 'eurs': eurs}


################################## veCurveVault tests #####################################
# pleb - small investor, malice - bad-actor
# In plain english:
# 1. Team deposits 1 weiCRV
# 2. Team claims 305 3CRV
# 3. Pleb deposits
# 4. Malice claims on empty vault after 100 days
# 5. Pleb claims on filled vault
# 6. Large depositor claims on empty vault after 50 days (with snapshot, revert to state after (2))
# 7. Malice claims on filled vault after 90 days (with snapshot, revert to state after (2))


def test_veCurveVault_team_deposit(deployedContracts):
    sender = deployedContracts['sender']
    DEFAULT_DEPLOYER_ACCOUNT = deployedContracts['DEFAULT_DEPLOYER_ACCOUNT']
    crv = deployedContracts['crv']
    crvBal = deployedContracts['crvBal']
    veCurve = deployedContracts['veCurve']
    votingEscrow = deployedContracts['votingEscrow']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']

    DEPOSIT_AMOUNT = 10**18
    crv.approve(veCurve.address, 10 * (10**6) * (10**18), sender)

    weightBefore = votingEscrow.balanceOf(curveYCRVVoter.address)
    lockedBefore = votingEscrow.locked(curveYCRVVoter.address)
    # sender is assumed as team's address
    veCurve.deposit(DEPOSIT_AMOUNT, sender)

    weightAfter = votingEscrow.balanceOf(curveYCRVVoter.address)
    lockedAfter = votingEscrow.locked(curveYCRVVoter.address)
    yveCrvBal = veCurve.balanceOf(DEFAULT_DEPLOYER_ACCOUNT)
    # lockedAfter[0] = amount, lockedAfter[1] = end
    assert yveCrvBal == DEPOSIT_AMOUNT
    assert weightAfter > weightBefore
    assert lockedAfter[0] == lockedBefore[0] + DEPOSIT_AMOUNT


def test_veCurveVault_team_claim(deployedContracts):
    sender = deployedContracts['sender']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']

    deployer3CrvBefore = threeCrv.balanceOf(sender['from'])
    yCrvVoter3CrvBefore = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvBefore = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvBefore team-claim', veCurve3CrvBefore)

    veCurve.claim(sender)

    deployer3CrvAfter = threeCrv.balanceOf(sender['from'])
    yCrvVoter3CrvAfter = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvAfter = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvAfter = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvAfter team-claim', veCurve3CrvAfter)

    assert deployer3CrvAfter > deployer3CrvBefore
    assert yCrvVoter3CrvAfter == yCrvVoter3CrvBefore
    assert stratProxy3CrvAfter == stratProxy3CrvBefore
    chain.snapshot()


def test_increase_unlock_time(deployedContracts):
    sender = deployedContracts['sender']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    crv = deployedContracts['crv']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    votingEscrow = deployedContracts['votingEscrow']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']

    # To 24/02/2022
    chain.sleep(365 * 1 * 84600)
    # 1738800000 = 06/02/2025
    lockedBefore = votingEscrow.locked(curveYCRVVoter.address)
    print("lockedBefore", lockedBefore[1])
    # 1758964777 = 24/9/2025
    data = votingEscrow.increase_unlock_time.encode_input(1766740777)
    curveYCRVVoter.execute(votingEscrow.address, 0, data, {
        'from': '0xf930ebbd05ef8b25b1797b9b2109ddc9b0d43063'})
    lockedAfter = votingEscrow.locked(curveYCRVVoter.address)
    print("lockedAfter", lockedAfter[1])
    assert lockedAfter[1] > lockedBefore[1]


def test_veCurveVault_pleb_deposit(deployedContracts):
    chain.revert()
    sender = deployedContracts['sender']
    crv = deployedContracts['crv']
    crvBal = deployedContracts['crvBal']
    veCurve = deployedContracts['veCurve']
    votingEscrow = deployedContracts['votingEscrow']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']

    DEPOSIT_AMOUNT = 100 * (10**18)
    crv.approve(veCurve.address, 10**9 * (10**18), pleb)

    weightBefore = votingEscrow.balanceOf(curveYCRVVoter.address)
    lockedBefore = votingEscrow.locked(curveYCRVVoter.address)

    veCurve.deposit(DEPOSIT_AMOUNT, pleb)

    weightAfter = votingEscrow.balanceOf(curveYCRVVoter.address)
    lockedAfter = votingEscrow.locked(curveYCRVVoter.address)
    yveCrvBal = veCurve.balanceOf(pleb['from'])
    # lockedAfter[0] = amount, lockedAfter[1] = end
    assert yveCrvBal == DEPOSIT_AMOUNT
    assert weightAfter > weightBefore
    assert lockedAfter[0] == lockedBefore[0] + DEPOSIT_AMOUNT


def test_malice_claim_on_empty_vault(deployedContracts):
    sender = deployedContracts['sender']
    DEFAULT_DEPLOYER_ACCOUNT = deployedContracts['DEFAULT_DEPLOYER_ACCOUNT']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']
    MALICE = '0x10Cdd8CDaa3c402AA2fc3d6a29b6D79424f77fDB'

    malice3CrvBefore = threeCrv.balanceOf(MALICE)
    vault3CrvBefore = threeCrv.balanceOf(veCurve.address)
    yCrvVoter3CrvBefore = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvBefore = threeCrv.balanceOf(STRATEGY_PROXY)
    print('veCurve3CrvBefore malice-claim', vault3CrvBefore)
    # 100 days in future to accumulate admin fees
    chain.sleep(100*24*60*60)
    # Malice trying to claim without depositing any CRV
    veCurve.claim({'from': MALICE})

    malice3CrvAfter = threeCrv.balanceOf(MALICE)
    vault3CrvAfter = threeCrv.balanceOf(veCurve.address)
    yCrvVoter3CrvAfter = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvAfter = threeCrv.balanceOf(STRATEGY_PROXY)
    print('veCurve3CrvAfter malice-claim', vault3CrvAfter)

    assert malice3CrvAfter == malice3CrvBefore
    assert vault3CrvAfter > vault3CrvBefore
    assert yCrvVoter3CrvAfter == yCrvVoter3CrvBefore
    assert stratProxy3CrvAfter == stratProxy3CrvBefore


def test_pleb_depositor_claim_on_filled_vault(deployedContracts):
    sender = deployedContracts['sender']
    DEFAULT_DEPLOYER_ACCOUNT = deployedContracts['DEFAULT_DEPLOYER_ACCOUNT']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']

    pleb3CrvBalBefore = threeCrv.balanceOf(pleb['from'])
    yCrvVoter3CrvBefore = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvBefore = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvBefore pleb-claim', veCurve3CrvBefore)
    # chain.sleep(100*24*60*60)
    veCurve.claim(pleb)
    veCurve.claim(pleb)

    pleb3CrvBalAfter = threeCrv.balanceOf(pleb['from'])
    yCrvVoter3CrvAfter = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvAfter = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvAfter = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvAfter pleb-claim', veCurve3CrvAfter)

    assert pleb3CrvBalAfter > pleb3CrvBalBefore
    assert yCrvVoter3CrvAfter == yCrvVoter3CrvBefore
    assert stratProxy3CrvAfter == stratProxy3CrvBefore


def test_large_depositor_claim_on_almost_empty_vault(deployedContracts):
    chain.revert()
    sender = deployedContracts['sender']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    crv = deployedContracts['crv']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    votingEscrow = deployedContracts['votingEscrow']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']
    CRV_WHALE = '0x0E33Be39B13c576ff48E14392fBf96b02F40Cd34'
    crv_whale = {'from': CRV_WHALE}

    crv.approve(veCurve.address, 10**9 * (10**18), crv_whale)
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)

    # assert veCurve3CrvBefore < 10**18
    # veCurve.deposit(100 * 10**18, crv_whale)
    veCurve.depositAll(crv_whale)
    chain.sleep(50*24*60*60)

    crvWhale3CrvBalBefore = threeCrv.balanceOf(CRV_WHALE)
    yCrvVoter3CrvBefore = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvBefore = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvBefore', veCurve3CrvBefore)

    veCurve.claim(crv_whale)

    crvWhale3CrvBalAfter = threeCrv.balanceOf(CRV_WHALE)
    yCrvVoter3CrvAfter = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvAfter = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvAfter = threeCrv.balanceOf(veCurve.address)
    print('veCurve3CrvAfter', veCurve3CrvAfter)

    assert crvWhale3CrvBalAfter > crvWhale3CrvBalBefore
    assert yCrvVoter3CrvAfter == yCrvVoter3CrvBefore
    assert stratProxy3CrvAfter == stratProxy3CrvBefore


def test_malice_claim_on_filled_vault(deployedContracts):
    chain.revert()
    sender = deployedContracts['sender']
    veCurve = deployedContracts['veCurve']
    curve3Pool = deployedContracts['curve3Pool']
    crv = deployedContracts['crv']
    threeCrv = deployedContracts['threeCrv']
    feeDistri = deployedContracts['feeDistri']
    votingEscrow = deployedContracts['votingEscrow']
    curveYCRVVoter = deployedContracts['curveYCRVVoter']
    pleb = deployedContracts['pleb']
    STRATEGY_PROXY = deployedContracts['STRATEGY_PROXY']
    MALICE_1 = '0x55FE002aefF02F77364de339a1292923A15844B8'
    MALICE_2 = '0xD6216fC19DB775Df9774a6E33526131dA7D19a2c'
    CRV_WHALE = '0xf89501b77b2fa6329f94f5a05fe84cebb5c8b1a0'
    crv_whale = {'from': CRV_WHALE}

    crv.approve(veCurve.address, 10**9 * (10**18), crv_whale)
    # veCurve.deposit(100 * 10**18, crv_whale)
    veCurve.depositAll(crv_whale)
    chain.sleep(90*24*60*60)

    crvWhale3CrvBalBefore = threeCrv.balanceOf(CRV_WHALE)
    yCrvVoter3CrvBefore = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvBefore = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)
    print("veCurve3CrvBefore malice1-claim 1", veCurve3CrvBefore)

    tx = veCurve.claim({'from': MALICE_1})
    # tx.call_trace()
    veCurve3CrvBefore = threeCrv.balanceOf(veCurve.address)
    print("veCurve3CrvBefore malice1-claim 2", veCurve3CrvBefore)
    # vault is now filled, though sometimes fees collected might be 0.1 3CRV
    assert veCurve3CrvBefore > 10**18
    malice2_3CrvBalBefore = threeCrv.balanceOf(MALICE_2)

    veCurve.claim({'from': MALICE_2})

    malice2_3CrvBalAfter = threeCrv.balanceOf(MALICE_2)
    yCrvVoter3CrvAfter = threeCrv.balanceOf(curveYCRVVoter.address)
    stratProxy3CrvAfter = threeCrv.balanceOf(STRATEGY_PROXY)
    veCurve3CrvAfter = threeCrv.balanceOf(veCurve.address)
    print("veCurve3CrvBefore malice1-claim 3", veCurve3CrvAfter)

    assert malice2_3CrvBalAfter == malice2_3CrvBalBefore
    assert veCurve3CrvAfter == veCurve3CrvBefore
    assert yCrvVoter3CrvAfter == yCrvVoter3CrvBefore
    assert stratProxy3CrvAfter == stratProxy3CrvBefore

################ StrategyProxy tests #########################


def test_strategyCurveEursCrvVoterProxy_approveStrategy(deployedContracts):
    strategyProxy = deployedContracts["strategyProxy"]
    strategyCurveEursCrvVoterProxy = deployedContracts["strategyCurveEursCrvVoterProxy"]
    deployer = deployedContracts["deployer"]

    # Register strategyCurveEursCrvVoterProxy in StrategyProxy
    # strategyProxy.approveStrategy(
    #     strategyCurveEursCrvVoterProxy.address, deployer)

    assert strategyProxy.strategies(
        strategyCurveEursCrvVoterProxy.address) == True


def test_strategyCurveEursCrvVoterProxy_setProxy(deployedContracts):
    strategyProxy = deployedContracts["strategyProxy"]
    strategyCurveEursCrvVoterProxy = deployedContracts["strategyCurveEursCrvVoterProxy"]
    deployer = deployedContracts["deployer"]

    # set proxy to StrategyProxy
    # strategyCurveEursCrvVoterProxy.setProxy(
    #     strategyProxy.address, deployer)

    assert strategyCurveEursCrvVoterProxy.proxy() == strategyProxy.address


def test_strategyCurveBTCVoterProxy_approveStrategy(deployedContracts):
    strategyProxy = deployedContracts["strategyProxy"]
    strategyCurveBTCVoterProxy = deployedContracts["strategyCurveBTCVoterProxy"]
    deployer = deployedContracts["deployer"]

    # Register strategyCurveBTCVoterProxy in StrategyProxy
    # strategyProxy.approveStrategy(strategyCurveBTCVoterProxy.address, deployer)

    assert strategyProxy.strategies(
        strategyCurveBTCVoterProxy.address) == True


def test_strategyCurve3CrvVoterProxy_approveStrategy(deployedContracts):
    strategyProxy = deployedContracts["strategyProxy"]
    strategyCurve3CrvVoterProxy = deployedContracts["strategyCurve3CrvVoterProxy"]
    deployer = deployedContracts["deployer"]

    # Register strategyCurve3CrvVoterProxy in StrategyProxy
    # strategyProxy.approveStrategy(
    #     strategyCurve3CrvVoterProxy.address, deployer)

    assert strategyProxy.strategies(
        strategyCurve3CrvVoterProxy.address) == True


def test_strategyProxy_setGovernance(deployedContracts):
    strategyProxy = deployedContracts["strategyProxy"]
    GNOSIS_SAFE_PROXY = deployedContracts["GNOSIS_SAFE_PROXY"]
    deployer = deployedContracts["deployer"]

    # Transfer StrategyProxy governance to Governance (GSP)
    # strategyProxy.setGovernance(GNOSIS_SAFE_PROXY, deployer)

    assert strategyProxy.governance() == GNOSIS_SAFE_PROXY


def test_veCurve_acceptGovernance(deployedContracts):
    veCurve = deployedContracts["veCurve"]
    GNOSIS_SAFE_PROXY = deployedContracts["GNOSIS_SAFE_PROXY"]
    multisig = deployedContracts["multisig"]

    # multisig accept Governance of veCurve vault
    # veCurve.acceptGovernance(multisig)

    assert veCurve.governance() == GNOSIS_SAFE_PROXY


def test_veCurve_setFeeDistribution(deployedContracts):
    veCurve = deployedContracts["veCurve"]
    strategyProxy = deployedContracts["strategyProxy"]
    multisig = deployedContracts["multisig"]

    # Set Curve FeeDistribution contract to new strategyProxy
    # veCurve.setFeeDistribution(strategyProxy.address, multisig)

    assert veCurve.feeDistribution() == strategyProxy.address


def test_veCurve_setProxy(deployedContracts):
    veCurve = deployedContracts["veCurve"]
    strategyProxy = deployedContracts["strategyProxy"]
    multisig = deployedContracts["multisig"]

    # Set new StrategyProxy
    # veCurve.setProxy(strategyProxy.address, multisig)

    assert veCurve.proxy() == strategyProxy.address


def test_strategyCurve3CrvVoterProxy_setProxy(deployedContracts):
    strategyCurve3CrvVoterProxy = deployedContracts["strategyCurve3CrvVoterProxy"]
    strategyProxy = deployedContracts["strategyProxy"]
    multisig = deployedContracts["multisig"]

    # set proxy to new StrategyProxy
    # strategyCurve3CrvVoterProxy.setProxy(strategyProxy.address, multisig)

    assert strategyCurve3CrvVoterProxy.proxy() == strategyProxy.address


def test_strategyCurveBTCVoterProxy_setProxy(deployedContracts):
    strategyCurveBTCVoterProxy = deployedContracts["strategyCurveBTCVoterProxy"]
    strategyProxy = deployedContracts["strategyProxy"]
    multisig = deployedContracts["multisig"]

    # set proxy to new StrategyProxy
    # strategyCurveBTCVoterProxy.setProxy(strategyProxy.address, multisig)

    assert strategyCurveBTCVoterProxy.proxy() == strategyProxy.address


def test_curveYCRVVoter_setStrategy(deployedContracts):
    curveYCRVVoter = deployedContracts["curveYCRVVoter"]
    strategyProxy = deployedContracts["strategyProxy"]
    multisig = deployedContracts["multisig"]

    # Set CurveYCRVVoter strategy to new StrategyProxy
    # curveYCRVVoter.setStrategy(strategyProxy.address, multisig)

    assert curveYCRVVoter.strategy() == strategyProxy.address


def test_eursCrvVault_earn(deployedContracts):
    strategyCurveEursCrvVoterProxy = deployedContracts["strategyCurveEursCrvVoterProxy"]
    deployer = deployedContracts["deployer"]
    eursCrvVault = deployedContracts["eursCrvVault"]
    EURS_CRV = deployedContracts["EURS_CRV"]
    eursCrv = deployedContracts["eursCrv"]
    strategyProxy = deployedContracts["strategyProxy"]
    curveYCRVVoter = deployedContracts["curveYCRVVoter"]
    controller = deployedContracts["controller"]

    totalBalBefore = eursCrvVault.balance()
    vaultBalBefore = eursCrvBal(deployedContracts, eursCrvVault.address)
    stratBalBefore = strategyCurveEursCrvVoterProxy.balanceOf()

    # assert stratBalBefore == 0
    # assert totalBalBefore == vaultBalBefore

    # Call earn on eursCrv Vault to transfer the funds to the new strategy
    eursCrvVault.earn(deployer)

    totalBalAfter = eursCrvVault.balance()
    vaultBalAfter = eursCrvBal(deployedContracts, eursCrvVault.address)
    stratBalAfter = strategyCurveEursCrvVoterProxy.balanceOf()

    assert totalBalBefore == totalBalAfter
    assert stratBalAfter > 0
    assert vaultBalBefore > vaultBalAfter
    assert vaultBalBefore < vaultBalAfter + stratBalAfter

    assert crvBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert eursCrvBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert eursBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert snxBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0

    assert crvBal(deployedContracts, strategyProxy) == 0
    assert eursCrvBal(deployedContracts, strategyProxy) == 0
    assert eursBal(deployedContracts, strategyProxy) == 0
    assert snxBal(deployedContracts, strategyProxy) == 0

    assert crvBal(deployedContracts, curveYCRVVoter) == 0
    assert eursCrvBal(deployedContracts, curveYCRVVoter) == 0
    assert eursBal(deployedContracts, curveYCRVVoter) == 0
    assert snxBal(deployedContracts, curveYCRVVoter) == 0

    assert crvBal(deployedContracts, controller) == 0
    assert eursCrvBal(deployedContracts, controller) == 0
    assert eursBal(deployedContracts, controller) == 0
    assert snxBal(deployedContracts, controller) == 0


def test_strategyCurveEursCrvVoterProxy_harvest(deployedContracts):
    strategyCurveEursCrvVoterProxy = deployedContracts["strategyCurveEursCrvVoterProxy"]
    deployer = deployedContracts["deployer"]
    eursCrvVault = deployedContracts["eursCrvVault"]
    multisig = deployedContracts["multisig"]
    strategyProxy = deployedContracts["strategyProxy"]
    curveYCRVVoter = deployedContracts["curveYCRVVoter"]
    votingEscrow = deployedContracts["votingEscrow"]
    controller = deployedContracts["controller"]
    treasuryVault = deployedContracts["treasuryVault"]

    chain.mine(1000)

    totalBalBefore = eursCrvVault.balance()
    stratBalBefore = strategyCurveEursCrvVoterProxy.balanceOf()
    earnedBefore = strategyCurveEursCrvVoterProxy.earned()
    lockedBefore = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalBefore = eursCrvBal(
        deployedContracts, treasuryVault.address)

    # assert earnedBefore == 0

    strategyCurveEursCrvVoterProxy.harvest(multisig)

    totalBalAfter = eursCrvVault.balance()
    stratBalAfter = strategyCurveEursCrvVoterProxy.balanceOf()
    earnedAfter = strategyCurveEursCrvVoterProxy.earned()
    lockedAfter = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalAfter = eursCrvBal(
        deployedContracts, treasuryVault.address)

    log("Total eursCrv Earned in 1000 blocks: " +
        str((earnedAfter-earnedBefore)/10**18))
    log("Change in total eursCrv in Vault+Strategy+Gauge: " +
        str((totalBalAfter-totalBalBefore)/10**18))
    log("Change in total eursCrv in Strategy+Gauge: " +
        str((stratBalAfter-stratBalBefore)/10**18))

    assert earnedAfter - earnedBefore > 0
    assert totalBalAfter > totalBalBefore
    assert stratBalAfter > stratBalBefore
    assert lockedAfter > lockedBefore
    assert treasuryVaultBalAfter > treasuryVaultBalBefore

    assert crvBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert eursCrvBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert eursBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0
    assert snxBal(deployedContracts, strategyCurveEursCrvVoterProxy) == 0

    assert crvBal(deployedContracts, strategyProxy) == 0
    assert eursCrvBal(deployedContracts, strategyProxy) == 0
    assert eursBal(deployedContracts, strategyProxy) == 0
    assert snxBal(deployedContracts, strategyProxy) == 0

    assert crvBal(deployedContracts, curveYCRVVoter) == 0
    assert eursCrvBal(deployedContracts, curveYCRVVoter) == 0
    assert eursBal(deployedContracts, curveYCRVVoter) == 0
    assert snxBal(deployedContracts, curveYCRVVoter) == 0

    assert crvBal(deployedContracts, controller) == 0
    assert eursCrvBal(deployedContracts, controller) == 0
    assert eursBal(deployedContracts, controller) == 0
    assert snxBal(deployedContracts, controller) == 0


def test_strategyCurve3CrvVoterProxy_harvest(deployedContracts):
    strategyCurve3CrvVoterProxy = deployedContracts["strategyCurve3CrvVoterProxy"]
    deployer = deployedContracts["deployer"]
    threePoolVault = deployedContracts["threePoolVault"]
    multisig = deployedContracts["multisig"]
    strategyProxy = deployedContracts["strategyProxy"]
    curveYCRVVoter = deployedContracts["curveYCRVVoter"]
    votingEscrow = deployedContracts["votingEscrow"]
    controller = deployedContracts["controller"]
    treasuryVault = deployedContracts["treasuryVault"]

    chain.mine(1000)

    totalBalBefore = threePoolVault.balance()
    stratBalBefore = strategyCurve3CrvVoterProxy.balanceOf()
    earnedBefore = strategyCurve3CrvVoterProxy.earned()
    lockedBefore = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalBefore = threeCrvBal(
        deployedContracts, treasuryVault.address)

    strategyCurve3CrvVoterProxy.harvest(multisig)

    totalBalAfter = threePoolVault.balance()
    stratBalAfter = strategyCurve3CrvVoterProxy.balanceOf()
    earnedAfter = strategyCurve3CrvVoterProxy.earned()
    lockedAfter = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalAfter = threeCrvBal(
        deployedContracts, treasuryVault.address)

    log("Total 3Crv Earned in 1000 blocks: " +
        str((earnedAfter-earnedBefore)/10**18))
    log("Change in total 3Crv in Vault+Strategy+Gauge: " +
        str((totalBalAfter-totalBalBefore)/10**18))
    log("Change in total 3Crv in Strategy+Gauge: " +
        str((stratBalAfter-stratBalBefore)/10**18))

    assert earnedAfter - earnedBefore > 0
    assert totalBalAfter > totalBalBefore
    assert stratBalAfter > stratBalBefore
    assert treasuryVaultBalAfter > treasuryVaultBalBefore

    assert crvBal(deployedContracts, strategyCurve3CrvVoterProxy) == 0
    assert threeCrvBal(deployedContracts, strategyCurve3CrvVoterProxy) == 0
    assert snxBal(deployedContracts, strategyCurve3CrvVoterProxy) == 0

    assert crvBal(deployedContracts, strategyProxy) == 0
    assert threeCrvBal(deployedContracts, strategyProxy) == 0
    assert snxBal(deployedContracts, strategyProxy) == 0

    assert crvBal(deployedContracts, curveYCRVVoter) == 0
    assert threeCrvBal(deployedContracts, curveYCRVVoter) == 0
    assert snxBal(deployedContracts, curveYCRVVoter) == 0
    assert lockedAfter > lockedBefore

    assert crvBal(deployedContracts, controller) == 0
    assert eursCrvBal(deployedContracts, controller) == 0
    assert eursBal(deployedContracts, controller) == 0
    assert snxBal(deployedContracts, controller) == 0


def test_strategyCurveBTCVoterProxy_harvest(deployedContracts):
    strategyCurveBTCVoterProxy = deployedContracts["strategyCurveBTCVoterProxy"]
    deployer = deployedContracts["deployer"]
    sbtcCrvVault = deployedContracts["sbtcCrvVault"]
    multisig = deployedContracts["multisig"]
    strategyProxy = deployedContracts["strategyProxy"]
    curveYCRVVoter = deployedContracts["curveYCRVVoter"]
    votingEscrow = deployedContracts["votingEscrow"]
    controller = deployedContracts["controller"]
    treasuryVault = deployedContracts["treasuryVault"]

    chain.mine(1000)

    totalBalBefore = sbtcCrvVault.balance()
    stratBalBefore = strategyCurveBTCVoterProxy.balanceOf()
    earnedBefore = strategyCurveBTCVoterProxy.earned()
    lockedBefore = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalBefore = sbtcCrvBal(
        deployedContracts, treasuryVault.address)

    strategyCurveBTCVoterProxy.harvest(multisig)

    totalBalAfter = sbtcCrvVault.balance()
    stratBalAfter = strategyCurveBTCVoterProxy.balanceOf()
    earnedAfter = strategyCurveBTCVoterProxy.earned()
    lockedAfter = votingEscrow.balanceOf(curveYCRVVoter.address)
    treasuryVaultBalAfter = sbtcCrvBal(
        deployedContracts, treasuryVault.address)

    log("Total sbtcCrv Earned in 1000 blocks: " +
        str((earnedAfter-earnedBefore)/10**18))
    log("Change in total sbtcCrv in Vault+Strategy+Gauge: " +
        str((totalBalAfter-totalBalBefore)/10**18))
    log("Change in total sbtcCrv in Strategy+Gauge: " +
        str((stratBalAfter-stratBalBefore)/10**18))

    assert earnedAfter - earnedBefore > 0
    assert totalBalAfter > totalBalBefore
    assert stratBalAfter > stratBalBefore
    assert treasuryVaultBalAfter > treasuryVaultBalBefore

    assert crvBal(deployedContracts, strategyCurveBTCVoterProxy) == 0
    assert sbtcCrvBal(deployedContracts, strategyCurveBTCVoterProxy) == 0
    assert snxBal(deployedContracts, strategyCurveBTCVoterProxy) == 0

    assert crvBal(deployedContracts, strategyProxy) == 0
    assert sbtcCrvBal(deployedContracts, strategyProxy) == 0
    assert snxBal(deployedContracts, strategyProxy) == 0

    assert crvBal(deployedContracts, curveYCRVVoter) == 0
    assert sbtcCrvBal(deployedContracts, curveYCRVVoter) == 0
    assert snxBal(deployedContracts, curveYCRVVoter) == 0
    assert lockedAfter > lockedBefore

    assert crvBal(deployedContracts, controller) == 0
    assert eursCrvBal(deployedContracts, controller) == 0
    assert eursBal(deployedContracts, controller) == 0
    assert snxBal(deployedContracts, controller) == 0


def crvBal(deployedContracts, address):
    crv = deployedContracts["crv"]
    return crv.balanceOf(address)


def eursCrvBal(deployedContracts, address):
    eursCrv = deployedContracts["eursCrv"]
    return eursCrv.balanceOf(address)


def eursBal(deployedContracts, address):
    eurs = deployedContracts["eurs"]
    return eurs.balanceOf(address)


def threeCrvBal(deployedContracts, address):
    threeCrv = deployedContracts["threeCrv"]
    return threeCrv.balanceOf(address)


def sbtcCrvBal(deployedContracts, address):
    sbtcCrvBal = deployedContracts["sbtcCrv"]
    return sbtcCrvBal.balanceOf(address)


def snxBal(deployedContracts, address):
    snx = deployedContracts["snx"]
    return snx.balanceOf(address)


def log(msg):
    msg = typer.style(msg, fg=typer.colors.GREEN, bold=True)
    typer.echo(msg)

    # DAI = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
    # USDC = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
    # USDC_WHALE = '0x55FE002aefF02F77364de339a1292923A15844B8'
    # dai = VaultToken.at(DAI)
    # usdc = VaultToken.at(USDC)
    # usdc.approve(curve3Pool.address, 10**9 * 10**6, {'from': USDC_WHALE})
    # dai.approve(curve3Pool.address, 10**9 * 10**18, {'from': USDC_WHALE})
    # # DAI = 0, USDC = 1, USDT = 2
    # curve3Pool.exchange(1, 0, 100 * 10**6 * 10**6, 10 *
    #                     10**18, {'from': USDC_WHALE})
    # print("DAI_BAL", dai.balanceOf(USDC_WHALE))

    # curve3Pool.exchange(0, 1, 99 * 10**6 * 10**18, 10 *
    #                     10**6, {'from': USDC_WHALE})
    # print("USDC_BAL", usdc.balanceOf(USDC_WHALE))
