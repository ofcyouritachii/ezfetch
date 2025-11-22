import platform
from typing import Optional
from pathlib import Path


# Logo definitions
LOGOS = {
    "arch": r"""                     
                  -`                     
                 .o+`                    
                `ooo/                    
               `+oooo:                   
              `+oooooo:                  
              -+oooooo+:                 
            `/:-:++oooo+:                
           `/++++/+++++++:               
          `/++++++++++++++:              
         `/+++ooooooooooooo/`            
        ./ooosssso++osssssso+`           
       .oossssso-````/ossssss+`          
      -osssssso.      :ssssssso.         
     :osssssss/        osssso+++.        
    /ossssssss/        +ssssooo/-        
  `/ossssso+/:-        -:/+osssso+-      
 `+sso+:-`                 `.-/+oso:     
`++:.                           `-/+/    
.`                                 `/    """,

    "debian": r"""
       _,met$$$$$gg.
    ,g$$$$$$$$$$$$$$$P.
  ,g$$P\"     \"\"\"Y$$.".
 ,$$P'              `$$$.
',$$P       ,ggs.     `$$b:
`d$$'     ,$P\"'   .    $$$
 $$P      d$'     ,    $$P
 $$:      $$.   -    ,d$$'
 $$;      Y$b._   _,d$P'
 Y$$.    `.`\"Y$$$$P\"'
 `$$b      \"-.__
  `Y$$
   `Y$$.
     `$$b.
       `Y$$b.
          `\"Y$b._
              `\"\"\"\" """,

    "ubuntu": r"""
            .-/+oossssoo+/-.
        `:+ssssssssssssssssss+:`
      -+ssssssssssssssssssyyssss+-
    .ossssssssssssssssss/    /ssssso.
   /sssssssssssssssss/      /ssssssss/
  +sssssssssssssss/        /ssssssssss+
 /ssssssssssssss/         /sssssssssssss
.ssssssssssssss+         +sssssssssssssss.
+ssssssssssssss/        /ssssssssssssssss+
ssssssssssssssss+/:  -/sssssssssssssssssss
ssssssssssssssssssssssssssssssssssssssssss
+ssssssssssssssssssssssssssssssssssssssss+
.ssssssssssssssssssssssssssssssssssssssss.
 /ssssssssssssssssssssssssssssssssssssss/
  +sssssssssssssssssssssssssssssssssss+
   /sssssssssssssssssssssssssssssssss/
    .ossssssssssssssssssssssssssssso.
      -+sssssssssssssssssssssssss+-
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.""",

    "mint": r"""
 MMMMMMMMMMMMMMMMMMMMMMMMMmds+.
 MMm----::-://////////////oymNMd+`
 MMd      /++                -sNMd:
 MMNso/`  dMM    `.::-. .-::.`/NMd
 ddddMMh  dMM   :hNMNMNhNMNMNh: `NMm
     NMm  dMM  .NMN/-+MMM+-/NMN` dMM
     NMm  dMM  -MMm  `MMM   dMM. dMM
     NMm  dMM  -MMm  `MMM   dMM. dMM
     NMm  dMM  .mmd  `mmm   yMM. dMM
     NMm  dMM`  ..`   ...   ydm. dMM
     hMM- +MMd/-------...-:sdds  dMM
     -NMm- :hNMNNNmdddddddddy/`  dMM
      -dMNs-``-::::-------.``    dMM
       `/dMNmy+/:-------------:/yMMM
          ./ydNMMMMMMMMMMMMMMMMMMMMM
             .MMMMMMMMMMMMMMMMMMM""",

    "mac": r"""
                    'c.
                 ,xNMM.
               .OMMMMo
               OMMM0,
     .;loddo:' loolloddol;.
   cKMMMMMMMMMMNWMMMMMMMMMM0:
 .KMMMMMMMMMMMMMMMMMMMMMMMWd.
 XMMMMMMMMMMMMMMMMMMMMMMMX.
;MMMMMMMMMMMMMMMMMMMMMMMM:
:MMMMMMMMMMMMMMMMMMMMMMMM:
.MMMMMMMMMMMMMMMMMMMMMMMMX.
 kMMMMMMMMMMMMMMMMMMMMMMMMWd.
 .XMMMMMMMMMMMMMMMMMMMMMMMMMMk
  .XMMMMMMMMMMMMMMMMMMMMMMMMK.
    kMMMMMMMMMMMMMMMMMMMMMMd
     ;KMMMMMMMWXXWMMMMMMMk.
       .cooc,.    .,coo:.""",

    "windows": r"""                                   
                                ..,
                    ....,,:;+ccllll
      ...,,+:;  cllllllllllllllllll
,cclllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
                                    
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
llllllllllllll  lllllllllllllllllll
`'ccllllllllll  lllllllllllllllllll
       `' \*::  :ccllllllllllllllll
                       ````''*::cll""",
    
    "fedora": r"""
          /:-------------:\          
       :-------------------::       
     :-----------/shhOHbmp---:\     
   /-----------omMMMNNNMMD  ---:   
  :-----------sMMMMNMNMP.    ---:  
 :-----------:MMMdP-------    ---\
,------------:MMMd--------    ---:
:------------:MMMd-------    .---:
:----    oNMMMMMMMMMNho     .----:
:--     .+shhhMMMmhhy++   .------/
:-    -------:MMMd--------------:
:-   --------/MMMd-------------;
:-    ------/hMMMy------------:
:-- :dMNdhhdNMMNo------------;
:---:sdNMMMMNds:------------:
:------:://:-------------::
:---------------------://""",

    "redhat": r"""                                   .
           .MMM..:MMMMMMM                   
          MMMMMMMMMMMMMMMM                  
          MMMMMMMMMMMMMMMMMM.              
         MMMMMMMMMMMMMMMMMMMM              
        ,MMMMMMMMMMMMMMMMMMMM:             
        MMMMMMMMMMMMMMMMMMMMMM             
  .MMMM'  MMMMMMMMMMMMMMMMMMMM            
 MMMMMM    `MMMMMMMMMMMMMMMMMM.             
MMMMMMMM      MMMMMMMMMMMMMMMM .          
MMMMMMMMM.       `MMMMMMMMMMM' MM.        
MMMMMMMMMMM.                     MM        
`MMMMMMMMMMMMM.                 MM'           
 `MMMMMMMMMMMMMMMMM.           MM'         
    MMMMMMMMMMMMMMMMMMMMMMMMMM'           
      MMMMMMMMMMMMMMMMMMMMM'              
         MMMMMMMMMMMMMMMM'                     
            `MMMMMMMM'                 
                                        """,
    
    "manjaro": r"""
██████████████████  ████████
██████████████████  ████████
██████████████████  ████████
██████████████████  ████████
████████            ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████
████████  ████████  ████████""",
    
    "popos": r"""
             /////////////
         /////////////////////
      ///////*767////////////////
    //////7676767676*//////////////
   /////76767//7676767//////////////
  /////767676///*76767///////////////
 ///////767676///76767.///7676*///////
/////////767676//76767///767676////////
//////////76767676767////76767/////////
///////////76767676//////7676//////////
////////////,7676,///////767///////////
/////////////*7676///////76////////////
///////////////7676////////////////////
 ///////////////7676///767////////////
  //////////////////////'////////////
   //////.7676767676767676767,//////
    /////767676767676767676767/////
      ///////////////////////////
         /////////////////////
             /////////////""",
    
    "alpine": r"""
       .hddddddddddddddddddddddh.
      :dddddddddddddddddddddddddd:
     /dddddddddddddddddddddddddddd/
    +dddddddddddddddddddddddddddddd+
  `sdddddddddddddddddddddddddddddddds`
 `ydddddddddddd++hdddddddddddddddddddy`
.hddddddddddd+`  `+ddddh:-sdddddddddddh.
hdddddddddd+`      `+y:    .sddddddddddh
ddddddddh+`   `//`   `.`     -sddddddddd
ddddddh+`   `/hddh/`   `:s-    -sddddddd
ddddh+`   `/+/dddddh/`   `+s-    -sddddd
ddd+`   `/o` :dddddddh/`   `oy-    .yddd
hdddyo+ohddyosdddddddddho+oydddy++ohdddh
.hddddddddddddddddddddddddddddddddddddh.
 `yddddddddddddddddddddddddddddddddddy`
  `sdddddddddddddddddddddddddddddddds`
    +dddddddddddddddddddddddddddddd+
     /dddddddddddddddddddddddddddd/
      :dddddddddddddddddddddddddd:
       .hddddddddddddddddddddddh.""",
    
    "gentoo": r"""
         -/oyddmdhs+:.
     -odNMMMMMMMMNNmhy+-`
   -yNMMMMMMMMMMMNNNmmdhy+-
 `omMMMMMMMMMMMMNmdmmmmddhhy/`
 omMMMMMMMMMMMNhhyyyohmdddhhhdo`
.ydMMMMMMMMMMdhs++so/smdddhhhhdm+`
 oyhdmNMMMMMMMNdyooydmddddhhhhyhNd.
  :oyhhdNNMMMMMMMNNNmmdddhhhhhyymMh
    .:+sydNMMMMMNNNmmmdddhhhhhhmMmy
       /mMMMMMMNNNmmmdddhhhhhmMNhs:
    `oNMMMMMMMNNNmmmddddhhdmMNhs+`
  `sNMMMMMMMMNNNmmmdddddmNMmhs/.
 /NMMMMMMMMNNNNmmmdddmNMNdso:`
+MMMMMMMNNNNNmmmmdmNMNdso/-
yMMNNNNNNNmmmmmNNMmhs+/-`
/hMMNNNNNNNNMNdhs++/-`
`/ohdmmddhys+++/:.`
  `-//////:--.""",
    
    "kali": r"""
      ,.....                                       
  ----`   `..,;:ccc,.                             
           ......''';lxO.                          
.....''''..........,:ld;                          
           .';;;:::;,,.x,                          
      ..'''.            0Xxoc:,.  ...              
  ....                ,ONkc;,;cokOdc',.            
 .                   OMo           ':do.           
                    dMc               :OO;         
                    0M.                 .:o.       
                    ;Wd                            
                     ;XO,                          
                       ,d0Odlc;,..                 
                           ..',;:cdOOd::,.         
                                    .:d;.':;.      
                                       'd,  .'     
                                         ;l   ..   
                                          .o       
                                            c      
                                            .'     
                                             .""",
}

# Add aliases
LOGOS["debian"] = LOGOS.get("debian", LOGOS["arch"])
LOGOS["ubuntu"] = LOGOS.get("ubuntu", LOGOS["arch"])
LOGOS["mint"] = LOGOS.get("mint", LOGOS["arch"])
LOGOS["redhat"] = LOGOS.get("redhat", LOGOS["arch"])
LOGOS["mac"] = LOGOS.get("mac", LOGOS["arch"])
LOGOS["windows"] = LOGOS.get("windows", LOGOS["arch"])
LOGOS["macos"] = LOGOS["mac"]
LOGOS["darwin"] = LOGOS["mac"]
LOGOS["pop"] = LOGOS["popos"]


def detect_distro() -> str:
    """
    Detect the current Linux distribution
    
    Returns:
        Distribution name in lowercase
    """
    os_name = platform.system().lower()
    
    if os_name == "linux":
        try:
            with open("/etc/os-release") as f:
                os_release = f.read().lower()
                
                # Check for specific distributions
                distros = [
                    "arch", "ubuntu", "debian", "mint", "fedora",
                    "manjaro", "popos", "pop", "alpine", "gentoo",
                    "kali", "red hat", "redhat"
                ]
                
                for distro in distros:
                    if distro in os_release:
                        return distro.replace(" ", "")
        except FileNotFoundError:
            pass
        
        return "arch"  # Default for Linux
    
    elif os_name == "darwin":
        return "mac"
    elif os_name == "windows":
        return "windows"
    
    return "arch"


def get_logo(logo_name: Optional[str] = None, custom_logo_path: Optional[str] = None) -> str:
    """
    Get ASCII art logo for current OS or specified logo
    
    Args:
        logo_name: Name of logo to use (overrides detection)
        custom_logo_path: Path to custom logo file
    
    Returns:
        ASCII art logo as string
    """
    # Use custom logo if provided
    if custom_logo_path:
        try:
            with open(custom_logo_path, "r") as f:
                return f.read()
        except (IOError, FileNotFoundError):
            pass
    
    # Use specified logo or detect
    distro = logo_name or detect_distro()
    return LOGOS.get(distro.lower(), LOGOS["arch"])


def list_logos() -> list:
    """
    Get list of available logo names
    
    Returns:
        List of logo names
    """
    return sorted(set(LOGOS.keys()))
