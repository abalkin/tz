import pytest
import base64
import io


@pytest.fixture(scope='session')
def zoneinfo(tmpdir_factory):
    """A fake zoneinfo tree."""
    tmpdir = tmpdir_factory.mktemp('zoneinfo')
    for zone, data in [('America/New_York', New_York),
                       ('Australia/Lord_Howe', Lord_Howe)]:
        infile = io.BytesIO(data)
        outpath = tmpdir.ensure(zone)
        with outpath.open('bw') as outfile:
            base64.decode(infile, outfile)
    with tmpdir.join('zone.tab').open('w') as f:
        f.write(ZONE_TAB)
    return tmpdir


@pytest.fixture
def ny_tzfile():
    data = base64.decodebytes(New_York)
    return io.BytesIO(data)


@pytest.fixture
def lh_tzfile():
    data = base64.decodebytes(Lord_Howe)
    return io.BytesIO(data)

ZONE_TAB = """\
US	+404251-0740023	America/New_York	Eastern (most areas)
AU	-3133+15905	Australia/Lord_Howe	Lord Howe Island
"""

# base64 -b 64 zoneinfo/America/New_York
New_York = b"""\
VFppZjIAAAAAAAAAAAAAAAAAAAAAAAAFAAAABQAAAAAAAADsAAAABQAAABSAAAAA
nqYecJ+662CghgBwoZrNYKJl4nCjg+ngpGqucKU1p2CmU8rwpxWJYKgzrPCo/qXg
qhOO8Kreh+Cr83DwrL5p4K3TUvCunkvgr7M08LB+LeCxnFFwsmdKYLN8M3C0Ryxg
tVwVcLYnDmC3O/dwuAbwYLkb2XC55tJguwT18LvGtGC85Nfwva/Q4L7EufC/j7Lg
wKSb8MFvlODChH3ww0924MRkX/DFL1jgxk18cMcPOuDILV5wyPhXYMoNQHDK2Dlg
y4jwcNIj9HDSYPvg03Xk8NRA3eDVVcbw1iC/4Nc1qPDYAKHg2RWK8Nngg+Da/qdw
28Bl4NzeiXDdqYJg3r5rcN+JZGDgnk1w4WlGYOJ+L3DjSShg5F4RcOVXLuDmRy3w
5zcQ4OgnD/DpFvLg6gbx8Or21ODr5tPw7Na24O3GtfDuv9Ng76/ScPCftWDxj7Rw
8n+XYPNvlnD0X3lg9U94cPY/W2D3L1pw+Ch34PkPPHD6CFng+vhY8PvoO+D82Drw
/cgd4P64HPD/p//gAJf+8AGH4eACd+DwA3D+YARg/XAFUOBgBkDfcAcwwmAHjRlw
CRCkYAmtlPAK8IZgC+CFcAzZouANwGdwDrmE4A+pg/AQmWbgEYll8BJ5SOATaUfw
FFkq4BVJKfAWOQzgFykL8BgiKWAZCO3wGgILYBryCnAb4e1gHNHscB3Bz2Aesc5w
H6GxYCB2APAhgZNgIlXi8CNqr+AkNcTwJUqR4CYVpvAnKnPgJ/7DcCkKVeAp3qVw
Kuo34Cu+h3As01RgLZ5pcC6zNmAvfktwMJMYYDFnZ/AycvpgM0dJ8DRS3GA1Jyvw
NjK+YDcHDfA4G9rgOObv8Dn7vOA6xtHwO9ue4Dyv7nA9u4DgPo/QcD+bYuBAb7Jw
QYR/YEJPlHBDZGFgRC92cEVEQ2BF86jwRy1f4EfTivBJDUHgSbNs8ErtI+BLnIlw
TNZAYE18a3BOtiJgT1xNcFCWBGBRPC9wUnXmYFMcEXBUVchgVPvzcFY1qmBW5Q/w
WB7G4FjE8fBZ/qjgWqTT8FveiuBchLXwXb5s4F5kl/Bfnk7gYE20cGGHa2BiLZZw
Y2dNYGQNeHBlRy9gZe1acGcnEWBnzTxwaQbzYGmtHnBq5tVga5Y68GzP8eBtdhzw
bq/T4G9V/vBwj7XgcTXg8HJvl+BzFcLwdE954HT+33B2OJZgdt7BcHgYeGB4vqNw
efhaYHqehXB72DxgfH5ncH24HmB+Xklwf5gAYAIBAgECAQIBAgECAQIBAgECAQIB
AgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIDBAIBAgECAQIBAgECAQIBAgEC
AQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgEC
AQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgEC
AQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgEC
AQIBAgECAQIBAgECAQIBAgECAQIBAgEC//+6ngAA///HwAEE//+5sAAI///HwAEM
///HwAEQTE1UAEVEVABFU1QARVdUAEVQVAAAAAAAAQAAAAABVFppZjIAAAAAAAAA
AAAAAAAAAAAAAAAFAAAABQAAAAAAAADtAAAABQAAABT4AAAAAAAAAP////9eA/CQ
/////56mHnD/////n7rrYP////+ghgBw/////6GazWD/////omXicP////+jg+ng
/////6RqrnD/////pTWnYP////+mU8rw/////6cViWD/////qDOs8P////+o/qXg
/////6oTjvD/////qt6H4P////+r83Dw/////6y+aeD/////rdNS8P////+unkvg
/////6+zNPD/////sH4t4P////+xnFFw/////7JnSmD/////s3wzcP////+0Ryxg
/////7VcFXD/////ticOYP////+3O/dw/////7gG8GD/////uRvZcP////+55tJg
/////7sE9fD/////u8a0YP////+85Nfw/////72v0OD/////vsS58P////+/j7Lg
/////8Ckm/D/////wW+U4P/////ChH3w/////8NPduD/////xGRf8P/////FL1jg
/////8ZNfHD/////xw864P/////ILV5w/////8j4V2D/////yg1AcP/////K2Dlg
/////8uI8HD/////0iP0cP/////SYPvg/////9N15PD/////1EDd4P/////VVcbw
/////9Ygv+D/////1zWo8P/////YAKHg/////9kVivD/////2eCD4P/////a/qdw
/////9vAZeD/////3N6JcP/////dqYJg/////96+a3D/////34lkYP/////gnk1w
/////+FpRmD/////4n4vcP/////jSShg/////+ReEXD/////5Vcu4P/////mRy3w
/////+c3EOD/////6CcP8P/////pFvLg/////+oG8fD/////6vbU4P/////r5tPw
/////+zWtuD/////7ca18P/////uv9Ng/////++v0nD/////8J+1YP/////xj7Rw
//////J/l2D/////82+WcP/////0X3lg//////VPeHD/////9j9bYP/////3L1pw
//////god+D/////+Q88cP/////6CFng//////r4WPD/////++g74P/////82Drw
//////3IHeD//////rgc8P//////p//gAAAAAACX/vAAAAAAAYfh4AAAAAACd+Dw
AAAAAANw/mAAAAAABGD9cAAAAAAFUOBgAAAAAAZA33AAAAAABzDCYAAAAAAHjRlw
AAAAAAkQpGAAAAAACa2U8AAAAAAK8IZgAAAAAAvghXAAAAAADNmi4AAAAAANwGdw
AAAAAA65hOAAAAAAD6mD8AAAAAAQmWbgAAAAABGJZfAAAAAAEnlI4AAAAAATaUfw
AAAAABRZKuAAAAAAFUkp8AAAAAAWOQzgAAAAABcpC/AAAAAAGCIpYAAAAAAZCO3w
AAAAABoCC2AAAAAAGvIKcAAAAAAb4e1gAAAAABzR7HAAAAAAHcHPYAAAAAAesc5w
AAAAAB+hsWAAAAAAIHYA8AAAAAAhgZNgAAAAACJV4vAAAAAAI2qv4AAAAAAkNcTw
AAAAACVKkeAAAAAAJhWm8AAAAAAnKnPgAAAAACf+w3AAAAAAKQpV4AAAAAAp3qVw
AAAAACrqN+AAAAAAK76HcAAAAAAs01RgAAAAAC2eaXAAAAAALrM2YAAAAAAvfktw
AAAAADCTGGAAAAAAMWdn8AAAAAAycvpgAAAAADNHSfAAAAAANFLcYAAAAAA1Jyvw
AAAAADYyvmAAAAAANwcN8AAAAAA4G9rgAAAAADjm7/AAAAAAOfu84AAAAAA6xtHw
AAAAADvbnuAAAAAAPK/ucAAAAAA9u4DgAAAAAD6P0HAAAAAAP5ti4AAAAABAb7Jw
AAAAAEGEf2AAAAAAQk+UcAAAAABDZGFgAAAAAEQvdnAAAAAARURDYAAAAABF86jw
AAAAAEctX+AAAAAAR9OK8AAAAABJDUHgAAAAAEmzbPAAAAAASu0j4AAAAABLnIlw
AAAAAEzWQGAAAAAATXxrcAAAAABOtiJgAAAAAE9cTXAAAAAAUJYEYAAAAABRPC9w
AAAAAFJ15mAAAAAAUxwRcAAAAABUVchgAAAAAFT783AAAAAAVjWqYAAAAABW5Q/w
AAAAAFgexuAAAAAAWMTx8AAAAABZ/qjgAAAAAFqk0/AAAAAAW96K4AAAAABchLXw
AAAAAF2+bOAAAAAAXmSX8AAAAABfnk7gAAAAAGBNtHAAAAAAYYdrYAAAAABiLZZw
AAAAAGNnTWAAAAAAZA14cAAAAABlRy9gAAAAAGXtWnAAAAAAZycRYAAAAABnzTxw
AAAAAGkG82AAAAAAaa0ecAAAAABq5tVgAAAAAGuWOvAAAAAAbM/x4AAAAABtdhzw
AAAAAG6v0+AAAAAAb1X+8AAAAABwj7XgAAAAAHE14PAAAAAAcm+X4AAAAABzFcLw
AAAAAHRPeeAAAAAAdP7fcAAAAAB2OJZgAAAAAHbewXAAAAAAeBh4YAAAAAB4vqNw
AAAAAHn4WmAAAAAAep6FcAAAAAB72DxgAAAAAHx+Z3AAAAAAfbgeYAAAAAB+Xklw
AAAAAH+YAGAAAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgEC
AQIBAgECAQIBAgMEAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIB
AgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIB
AgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIB
AgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIBAgECAQIB
AgECAQL//7qeAAD//8fAAQT//7mwAAj//8fAAQz//8fAARBMTVQARURUAEVTVABF
V1QARVBUAAAAAAABAAAAAAEKRVNUNUVEVCxNMy4yLjAsTTExLjEuMAo=
"""

# base64 -b 64 zoneinfo/Australia/Lord_Howe
Lord_Howe = b"""\
VFppZjIAAAAAAAAAAAAAAAAAAAAAAAAFAAAABQAAAAAAAABzAAAABQAAABOAAAAA
FP5m4BY4QPgW54poGCFdeBjHbGgaAT94GqdOaBvhIXgchzBoHcEDeB55jnAfl6r4
IFlwcCGAx3giQozwI2nj+CQibvAlScX4Je/b8Ccpp/gnz73wKQmJ+Cmvn/Aq6Wv4
K5i8cCzSiHgteJ5wLrJqeC9YgHAwkkx4MV1McDJyLngzPS5wNFIQeDUdEHA2MfJ4
NvzycDgbDvg43NRwOafieDq8tnA72tL4PKXS8D26tPg+hbTwP5qW+EBllvBBg7N4
QkV48ENjlXhELpVwRUN3eEYFPPBHI1l4R/eT8Ejni/hJ13XwSsdt+Eu3V/BMp0/4
TZc58E6HMfhPdxvwUHBOeFFgOHBSUDB4U0AacFQwEnhVH/xwVg/0eFb/3nBX79Z4
WN/AcFnPuHhav6JwW7jU+FyovvBdmLb4Xoig8F94mPhgaILwYVh6+GJIZPBjOFz4
ZChG8GUYPvhmEWNwZwFbeGfxRXBo4T14adEncGrBH3hrsQlwbKEBeG2Q63BugON4
b3DNcHBp//hxWenwcknh+HM5y/B0KcP4dRmt8HYJpfh2+Y/wd+mH+HjZcfB5yWn4
erlT8Huyhnh8onBwfZJoeH6CUnB/ckp4AQMCAwIDAgMCAwQDBAMEAwQDBAMEAwQD
BAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQD
BAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAAAlSQA
AAAAjKAABAAAobgBCQAAk6gADgAAmrABCUxNVABBRVNUAExIRFQATEhTVAAAAAAA
AAAAAAAAVFppZjIAAAAAAAAAAAAAAAAAAAAAAAAFAAAABQAAAAAAAAB0AAAABQAA
ABP4AAAAAAAAAP////9zFnfcAAAAABT+ZuAAAAAAFjhA+AAAAAAW54poAAAAABgh
XXgAAAAAGMdsaAAAAAAaAT94AAAAABqnTmgAAAAAG+EheAAAAAAchzBoAAAAAB3B
A3gAAAAAHnmOcAAAAAAfl6r4AAAAACBZcHAAAAAAIYDHeAAAAAAiQozwAAAAACNp
4/gAAAAAJCJu8AAAAAAlScX4AAAAACXv2/AAAAAAJymn+AAAAAAnz73wAAAAACkJ
ifgAAAAAKa+f8AAAAAAq6Wv4AAAAACuYvHAAAAAALNKIeAAAAAAteJ5wAAAAAC6y
angAAAAAL1iAcAAAAAAwkkx4AAAAADFdTHAAAAAAMnIueAAAAAAzPS5wAAAAADRS
EHgAAAAANR0QcAAAAAA2MfJ4AAAAADb88nAAAAAAOBsO+AAAAAA43NRwAAAAADmn
4ngAAAAAOry2cAAAAAA72tL4AAAAADyl0vAAAAAAPbq0+AAAAAA+hbTwAAAAAD+a
lvgAAAAAQGWW8AAAAABBg7N4AAAAAEJFePAAAAAAQ2OVeAAAAABELpVwAAAAAEVD
d3gAAAAARgU88AAAAABHI1l4AAAAAEf3k/AAAAAASOeL+AAAAABJ13XwAAAAAErH
bfgAAAAAS7dX8AAAAABMp0/4AAAAAE2XOfAAAAAATocx+AAAAABPdxvwAAAAAFBw
TngAAAAAUWA4cAAAAABSUDB4AAAAAFNAGnAAAAAAVDASeAAAAABVH/xwAAAAAFYP
9HgAAAAAVv/ecAAAAABX79Z4AAAAAFjfwHAAAAAAWc+4eAAAAABav6JwAAAAAFu4
1PgAAAAAXKi+8AAAAABdmLb4AAAAAF6IoPAAAAAAX3iY+AAAAABgaILwAAAAAGFY
evgAAAAAYkhk8AAAAABjOFz4AAAAAGQoRvAAAAAAZRg++AAAAABmEWNwAAAAAGcB
W3gAAAAAZ/FFcAAAAABo4T14AAAAAGnRJ3AAAAAAasEfeAAAAABrsQlwAAAAAGyh
AXgAAAAAbZDrcAAAAABugON4AAAAAG9wzXAAAAAAcGn/+AAAAABxWenwAAAAAHJJ
4fgAAAAAcznL8AAAAAB0KcP4AAAAAHUZrfAAAAAAdgml+AAAAAB2+Y/wAAAAAHfp
h/gAAAAAeNlx8AAAAAB5yWn4AAAAAHq5U/AAAAAAe7KGeAAAAAB8onBwAAAAAH2S
aHgAAAAAfoJScAAAAAB/ckp4AAEDAgMCAwIDAgMEAwQDBAMEAwQDBAMEAwQDBAME
AwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAME
AwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQDBAMEAwQAAJUkAAAAAIyg
AAQAAKG4AQkAAJOoAA4AAJqwAQlMTVQAQUVTVABMSERUAExIU1QAAAAAAAAAAAAA
AApMSFNULTEwOjMwTEhEVC0xMSxNMTAuMS4wLE00LjEuMAo=
"""
