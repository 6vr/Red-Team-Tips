Anatomy of an Attack
================================================================================

<br>

<details>
  <summary><b><u>
  Intro
  </u></b></summary>
  
No single workflow works for every attack. Even attempting to generalize the workflow to allow for 90% of encounters still includes a bunch of 'gotchas' along the way. I still advocate for a comprehensive framework of general and specific cheat sheets, but the framework won't get you too far unless you understand which sheet to use at which point. In other words, you need to understand the general flow of an attack (whether remote, client-side, or physical).

In the rest of this article, I do my best to combine several of the actions one might perform during an attack with the classic 9-part "Anatomy of an Attack". We have a few problems. First, the classic model includes a section titled "Scanning", but it only clearly describes remote attacks. The classic model is fairly old and, in my opinion, obsolete for this type of generalized framework. Second, during any attack, you'll likely //enumerate// the target several times: once before deciding if it is a good initial target, again when identifying a vulnerability you can exploit for access, yet again to elevate your privileges once on the target, and at least once more to pilfer what you want. How do you capture all of that? Third, most models fail to encompass supporting actions, such as securing a network foothold, even though they're often the most difficult actions to execute. Last, how many models out there include WiFi exploitation as an attack vector to secure a foothold on a target network?

I don't have a magic pill that will convert the very non-linear attack workflow into an easy-to-write, linear process. I also can't let everything sit at "you'll learn on the job" or "you should teach yourself through experience". You ought to have some mental framework ready so you can categorize everything you learn. So, hopefully the remainder of this article will help. Read it in the order it's printed, as I think that highlights where additional thought is necessary.

It's hard to put a picture of "thinking outside the box" into a box.

<br>
</details>

<details>
  <summary><b><u>
  What Theory Says You Do
  </u></b></summary>

<u>The Classic Model</u>

**Footprinting** - Target address range, namespace acquisition, and information gathering are essential to a surgical attack. The key here is not to miss any details. 

**Scanning** - Bulk target assessment and identification of listening services focus the attacker's attention on the most promising avenues of entry. 

**Enumeration** - More intrusive probing now begins as attackers begin identifying valid user accounts or poorly protected resource shares. 

**Gaining Access** - Enough data has been gathered at this point to make an informed attempt to access the target. If unsuccessful, jump to "Denial of Service". 

**Escalating Privilege** - If only user-level access was obtained in the last step, the attacker will now seek to gain complete control of the system. 

**Pilfering** - The information-gathering process begins again to identify mechanisms to gain access to trusted systems. Jump back to "Enumeration" if you want to move to other systems. 

**Covering Tracks** - Once total ownership of the target is secured, hiding the fact from system administrators becomes paramount, lest they quickly end the romp. 

**Creating Backdoors** - Trap doors will be laid in various parts of the system to ensure that privileged access is easily regained at the whim of the intruder. 

**Denial of Service** - If an attacker is unsuccessful in gaining access, they may use readily available exploit code to disable a target as a last resort. 

<br>
</details>

<details>
  <summary><b><u>
  What You Actually Do
  </u></b></summary>

1. <u>Prep</u>
  1. **Recon** attack surfaces
     - OSINT
     - Surveillance
  2. **Decide**
     - Attack vectors
     - Footholds
     - OBJs
     - Actions on OBJs
2. <u>Execute loop, like `while true:`</u>
  3. **Enumerate**
     - NetBios scan
     - Traffic capture
     - Portscan
     - Vulscan
  4. **Exploit**
     - Remote
     - Local
     - Out-of-band
     - Privilege escalation
     - DoS
  5. **Post-Ex**
     - Gather tools
     - Persistence
     - Cover traces
     - Pilfer
  6. `if (rooted == true && pilfered == true): break`


<br>
</details>

<details>
  <summary><b><u>
  What This Actually Looks Like
  </u></b></summary>

*An example...*

<u>#1 Remote & Local Recon</u>

1. Assess target's cyber attack surfaces. (On Atk Sys) 
2. Find web apps and services.
3. Enumerate web apps and services.
4. Identify potential remote footholds.
5. Geolocate LANs.
6. Visit and enumerate LANs.
7. Identify potential local footholds. 

<u>#2 Seize a Foothold</u>

1. Choose best foothold, whether remote or on a LAN.
2. Enumerate foothold for exploit.
3. Prepare tools (jumps, leave-behinds, malware). 
4. Exploit foothold and gain access. (On the foothold)
5. Post-exploitation.
6. Enumeration.
7. Escalate privileges on foothold.
8. Build persistence on foothold.
9. Post-exploitation as required.
10. Gather tools for follow-on attack. 

<u>#3 Attack the Objective</u>

1. Use foothold to enumerate the objective.
2. Exploit the objective and gain access. (On the OBJ) 
3. Post-exploitation.
4. Build initial persistence. (Optional)
5. Enumeration.
6. Escalate privileges on objective.
7. Change persistence to privileged persistence.
8. Post-exploitation.
9. Deliver desired effects. 

*Terminology:*

- Target - The person (e.g., bad guy) or organization (e.g., crime ring) you want to capture, kill, disrupt, or apply other effects against.
- Objective aka OBJ - The item, data, function, or place that hackers can manipulate in support of prosecuting the Target. Usually belongs to or enables the Target in some manner. 

<br>
</details>
