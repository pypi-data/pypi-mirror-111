# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from collections import OrderedDict
from nettoolkit import IPv4, IPv6, STR, LST

from .tasks import Tasks
from .templates import iftype_templ, ParametersTemplate as para

# ----------------------------------------------------------------------------
# Device / IDENTIFIERS/ STARTERS/ COLUMN INDEXES - JUNIPER
# ----------------------------------------------------------------------------

JUNIPER_IFS_IDENTIFIERS = {
	"VLAN": ('irb', 'vlan'),
	"LOOPBACK": 'lo',
	"RANGE": 'interface-range',
	"TUNNEL": ('lt',),
	"AGGREGATED": ('ae',),
	"PHYSICAL": ('ge', 'xe', ),
	"MANAGEMENT": ('mg', 'em', 'me', 'fxp'),
}
JUNIPER_STARTERS = {
	'ifs': 'set interfaces',
	'vrfs': 'set routing-instances',
	'vlans': ('set bridge-domains', 'set vlan', ),
}

# ---------------------------------------------------------------------------- #
# Juniper TASKS
# ---------------------------------------------------------------------------- #

class JuniperTasks(Tasks):
	"""Juniper Tasks"""

	ifs_identifiers = JUNIPER_IFS_IDENTIFIERS
	starter = JUNIPER_STARTERS

	def get_section_config(self, section, name, af_only=False):
		"""--> Section config in list format"""
		section_config = []
		start = False
		for line in self.run_list:
			start_section = self.starter[section]
			spl = line.split()
			if section == 'ifs':
				if spl[2] == 'irb':
					start_section = " ".join(spl[:4])
				elif spl[2].startswith(self.ifs_identifiers['LOOPBACK']):
					try:
						start_section = " ".join(spl[:4])
					except: continue
				elif spl[2] == self.ifs_identifiers['RANGE']:
					start_section = " ".join(spl[:3])

			elif section == 'vlans':
				start_section = " ".join(spl[:2])

			start = line.startswith(start_section + " " + str(name) + " ")
			if start:
				section_config.append(line.rstrip())
		return section_config

	""" AAZA """

	def aaza(self):
		"""Aaza of device"""
		for line in self.run_list:
			# Interfaces configs
			if line.startswith(self.starter['ifs']):
				self.aaza_ifs(line)
				continue
			# vrf definitions
			if line.startswith(self.starter['vrfs']):
				self.aaza_vrfs(line)
				continue
			# vlans
			if (line.startswith(self.starter['vlans'][0])
				or line.startswith(self.starter['vlans'][1])
				) and STR.found(line, 'vlan-id'):
				self.aaza_vlans(line)
				continue
			# snmp string
			if line.startswith("set snmp location"):
				if line[18] == '"':
					self.snmp_location = line[19:].strip()
				else:
					self.snmp_location = line[18:].strip()					
			# exec banner
			if line.startswith("set system login announcement"):
				self.banner = line[30:].strip()

		return {'if_types': self.if_types, 
				'ifs': self.ifs, 
				'vrfs': self.vrfs, 
				'vlans': self.vlans,
				'ospf': self.ospf,
				'bgp': self.bgp,
				'bgp_af': self.bgp_af,
				}

	def aaza_vrfs(self, line):
		"""add new vrf to aaza"""
		spl = line.split()
		if spl[2] not in self.vrfs:
			self.vrfs.append(spl[2])

	def aaza_vlans(self, line):
		"""add new vlan to aaza"""
		spl = line.split()
		vlan = int(spl[-1])
		self.add_aaza(vlan, self.ifvlans, para.ifvlan)
		self.ifvlans[vlan]['vl_identifier'] = spl[2]

	def aaza_ifs(self, line):
		"""add new interface to aaza"""
		spl = line.split()
		if spl[2] in ('irb', 'vlan'):
			vlan = int(spl[4])
			self.add_aaza(vlan, self.ifvlans, para.ifvlan)
		elif spl[2].startswith(self.ifs_identifiers['LOOPBACK']):
			try:
				unit = int(spl[4])
				self.add_aaza(unit, self.ifloopbacks, para.ifloopback)
			except: pass
		elif spl[2] == self.ifs_identifiers['RANGE']:
			range_name = spl[3]
			self.add_aaza(range_name, self.ifranges, para.ifrange)
		else:
			for int_type, int_types in self.ifs_identifiers.items():
				if int_type in ("VLAN", "LOOPBACK", "RANGE"): continue
				for int_type_type in int_types:
					if int_type_type in spl[2]:
						self.add_aaza(spl[2], self.iftype_ifvar[int_type], iftype_templ(int_type))

	def interface_aaza(self):
		"""Interface Aaza from interface status"""
		headers = None
		self.interfaces_table = {}
		for line in self.int_status_list:
			if STR.is_blank_line(line): continue
			if headers is None:
				headers = STR.header_indexes(line)
				del(headers["Description"])
				continue
			else:
				for header_item, idxes in headers.items():
					detail = line[idxes[0]:idxes[1]].strip()
					if header_item == 'Interface':
						if not self.interfaces_table.get(detail):
							self.interfaces_table[detail] = {}
							port_detail = self.interfaces_table[detail]
							continue
					port_detail[header_item] = detail
				port_detail['adminstatus'] = port_detail['Admin']
				port_detail['linkstatus'] = port_detail['Link']
				del(port_detail['Admin'])
				del(port_detail['Link'])

	def lldp_aaza(self):
		"""lldp aaza from lldp neighbors"""
		self.lldp_table = {}
		for line in self.lldp_list:
			if STR.is_blank_line(line): continue
			if line.startswith("Local Interface"): continue
			spl = line.split()
			local_if = spl[0].split(".")[0]
			neighbor_name = spl[-1].strip()
			neighbor_if = spl[-2]
			## Note: 'Device ID' = System Name, 'Port ID' = Port info ##
			self.lldp_table[local_if] =  {'Device ID': neighbor_name,
											'Port ID': neighbor_if}

	""" Facts """

	def get_facts_hostname(self):
		"""device hostname"""
		for line in self.run_list:
			if line.startswith("set system host-name "):
				self.var['hostname'] = line.split()[-1]
				# self.facts['[dev_hostname]'] = line.split()[-1]
				break

	def get_facts_interfaces(self):
		"""Interface Facts"""
		for ifType in self.if_types:
			facts_if = self.iftype_ifvar[ifType]
			for _if, ifFacts in facts_if.items():
				section_conf = self.get_section_config('ifs', _if)
				ifFacts['shortname'] = _if
				try:
					ifFacts['int_number'] = int(_if)
				except:
					ifFacts['int_number'] = None
				test = ifType == "PHYSICAL"
				ifFacts['description'] = self.int_description(section_conf)
				ifFacts['adminstatus'] = self.int_port_status(section_conf)
				ifFacts['udld'] = self.int_udld_state(section_conf)
				ifFacts.update(self.int_ether_channel(section_conf))
				if ifType not in ('VLAN', 'LOOPBACK'):
					ifFacts['switchport'] = self.int_vlans(section_conf)
				if ifType not in ('VLAN', 'MANAGEMENT'):
					ifFacts['l2orl3'] = self.get_l2orl3(section_conf)
				if ifType in ("AGGREGATED", ) and ifFacts['l2orl3'] == 'l2':
					ifFacts['vlanmembers'] = self.int_vlan_members(section_conf)
				else:
					ifFacts.update(self.int_address(section_conf, test))

	def int_vlan_members(self, int_section_config):
		"""aggregated interface member vlan/subint"""
		members = set()
		for line in int_section_config:
			spl = line.split()
			if spl[3] == 'unit':
				members.add(int(spl[4]))
		return members

	def get_facts_vrfs(self):
		"""vrf Facts"""
		self.facts["vrfs"] = OrderedDict()
		facts_vrfs = self.facts["vrfs"]
		for vrf in self.vrfs:
			section_conf = self.get_section_config('vrfs', vrf)
			self.vrf_int_vrf(section_conf)
			self.vrf_int_helpers(section_conf)
			facts_vrfs[vrf] = self.vrf_rd_rt(section_conf)
			facts_vrfs[vrf].update({'vrf': vrf})

	def get_facts_vlans(self):
		super().get_facts_vlans('juniper')

	def get_facts_static(self):
		"""static route facts"""
		self.facts["statics"] = OrderedDict()
		self.facts["statics"].update(self.static_route())

	def get_facts_ospf(self):
		"""ospf facts"""
		self.facts["ospf"] = {}
		self.facts["ospf"].update(self.ospf_all())

	def get_facts_bgp(self, isInstance=False):
		"""bgp facts"""
		if isInstance: return None
		self.facts["bgp"] = {}
		self.facts["bgp"].update(self.bgp_all())

	""" VLAN """
	def vlan_name(self, int_section_config):
		"""set vlan name for each vlans"""
		name = ''
		for line in int_section_config:
			if STR.found(line, "description"):
				spl = line.split()
				desc_idx = spl.index('description') + 1
				name = " ".join(spl[desc_idx:])
				break
		return name

	""" VRF """

	def vrf_rd_rt(self, int_section_config):
		"""vrf rd/rt aaza"""
		router_id, rd, rt_import, rt_export = '', '', '', ''
		for line in int_section_config:
			if STR.found(line, "route-distinguisher"):
				rd = line.split()[-1]
				router_id = rd.split(":")[0]
				continue
			if STR.found(line, "vrf-target export"):
				rt_export = ":".join(line.split()[-1].split(":")[-2:])
				continue
			if STR.found(line, "vrf-target import"):
				rt_import = ":".join(line.split()[-1].split(":")[-2:])
				continue
		return {'router_id': router_id,
				'rd': rd, 
				'rt_export': rt_export, 
				'rt_import':rt_import}

	def vrf_int_vrf(self, int_section_config):
		"""set vrf for particular interfaces"""
		# not satisfied with this function.
		for line in int_section_config:
			spl = line.split()
			if spl[3] == 'interface':
				vrf_int = spl[-1]
				ifType = self.int_type(vrf_int)
				# -------------------------------
				# doubtful - double check below 
				if ifType in ("VLAN", "LOOPBACK"):
					_if = int(spl[-1].split(".")[-1])
				else:
					_if = spl[-1].split(".")[0]
				# -------------------------------
				if self.iftype_ifvar[ifType].get(_if):
					self.iftype_ifvar[ifType][_if]['vrf'] = spl[2]

	def vrf_int_helpers(self, int_section_config):
		"""set helper ip's for particular interface"""
		helpers = self.vrf_helpers(int_section_config)
		# not satisfied with this function.
		for line in int_section_config:
			spl = line.split()
			if spl[-2] == 'interface':
				vrf_int = spl[-1]
				ifType = self.int_type(vrf_int)
				# -------------------------------
				# doubtful - double check below 
				if ifType in ("VLAN", ):
					_if = int(spl[-1].split(".")[-1])
				else:
					_if = spl[-1].split(".")[0]
				# -------------------------------
				if self.iftype_ifvar[ifType].get(_if):
					self.iftype_ifvar[ifType][_if].update(helpers)

	def vrf_helpers(self, int_section_config):
		"""set helper ip's for particular vrf's"""
		helpers, v6helpers = [], []
		for line in int_section_config:
			spl = line.split()
			if STR.found(line, 'dhcp-relay server-group'):
				helpers.append(spl[-1])
			if STR.found(line, 'dhcp-relay dhcpv6 server-group'):
				v6helpers.append(spl[-1])
		return {'dhcphelpers': helpers, 
				'dhcpv6helpers': v6helpers}

	""" Interfaces """

	def get_l2orl3(self, int_section_config):
		"""interface type - L2 or L3 """
		l2orl3 = 'l3'
		for line in int_section_config:
			spl = line.split()
			try:
				if spl[3] == 'unit' and (1 <= int(spl[4]) <= 4092 or STR.found(line, 'vlan members')):
					l2orl3 = 'l2'
					break
			except: continue
		return l2orl3

	def int_port_status(self, int_section_config):
		"""status of port"""
		status = 'up'
		for line in int_section_config:
			if STR.found(line, "disable"):
				status = 'down'
				break
		return status

	def int_udld_state(self, int_section_config):
		"""interface udld status"""
		# not available for Juniper
		udld = 'disable'
		return udld

	def int_type(self, interface):
		"""--> Interface Type for given input interface"""
		if STR.found(interface, 'irb') or STR.found(interface, 'vlan'):
			return 'VLAN'
		elif interface.startswith(self.ifs_identifiers['LOOPBACK']):
			return 'LOOPBACK'
		else:
			for int_type, int_types in self.ifs_identifiers.items():
				if int_type in ("VLAN", "LOOPBACK", "RANGE"): continue
				for int_type_type in int_types:
					if int_type_type in interface:
						return int_type
		
	def int_address(self, int_section_config, test=False):
		"""IP Addressing on interface"""
		subnet = ''
		v6subnet = ''
		linklocal = ''
		v6linklocal = ('fe80::',)
		for line in int_section_config:
			# if test: print(line)
			if not subnet and STR.found(line, "family inet address "):
				spl = line.split()
				ip_idx = spl.index('inet') + 2
				ip = spl[ip_idx]
				subnet = IPv4(ip)
				continue
			if not v6subnet and STR.found(line, "family inet6 address "):
				spl = line.split()
				ip_idx = spl.index('inet6') + 2
				ip = spl[ip_idx]
				exclude = False
				for evc in v6linklocal:
					if STR.found(ip, evc): 
						exclude = True
						linklocal = IPv6(ip)
						break
				if exclude: continue
				v6subnet = IPv6(ip)
				break
		address_vars = {
			'inet4': {'address': subnet },
			'inet6': {'address': v6subnet, 'linklocal': linklocal},
			}
		return address_vars

	def int_vlans(self, int_section_config):
		"""Switching on interface"""
		mode = None
		access_vlan = 1
		voice_vlan = None
		native_vlan = 1
		trunk_vlans = []
		for line in int_section_config:
			if STR.found(line, "interface-mode"):
				mode = line.split()[-1]
				continue
			# juniper native vlan not found to be add if found here.
			if mode == 'access' and (STR.found(line, "bridge vlan-id-list") or STR.found(line, "members")):
				access_vlan = int(line.split()[-1])
				continue
			if mode == 'trunk' and (STR.found(line, "bridge vlan-id-list") or STR.found(line, "members")):
				for v in self.get_vlans_from_range(line.split()[-1]):
					for x in v: trunk_vlans.append(int(x))
				continue
			### Voice vlan set - to be implemented
		return {'mode': mode,
				'accessvlan': access_vlan,
				'nativevlan': native_vlan,
				'voicevlan': voice_vlan,
				'trunkvlans': trunk_vlans,
				}

	def int_ether_channel(self, int_section_config):
		"""Port Channel config on interface"""
		channel_group = None
		channel_group_mode = None
		for line in int_section_config:
			if STR.found(line, "802.3ad"):
				spl = line.split()
				channel_group = spl[-1]
				section_conf = self.get_section_config('ifs', channel_group)
				channel_group_mode = self.int_ether_channel_mode(section_conf)
				break
		return {'ponumber': channel_group,
				'pomode': channel_group_mode,}

	def int_ether_channel_mode(self, int_section_config):
		"""-->Port Channel mode on interface / child"""
		channel_group_mode = None
		for line in int_section_config:
			if STR.found(line, 'aggregated-ether-options lacp '):
				spl = line.split()
				channel_group_mode = spl[-1]
				break
		return channel_group_mode

	""" Statics """

	def static_route(self):
		"""--> static route parameters """
		routes, route, vrf, name, tag, next_hop, prev_route = {}, None, None, None, None, None, 'None'
		for line in self.run_list:
			if STR.found(line, "routing-options static route"):
				spl = line.split()
				route_idx = spl.index("route") + 1
				subnet = IPv4(spl[route_idx])
				vrf = spl[2] if spl[1] == 'routing-instances' else None
				tag = spl[-1] if STR.found(line, "tag") else None
				subnet_header = vrf + "_" + str(subnet) if vrf else str(subnet)				
				next_hop = IPv4(spl[-1]+"/32") if STR.found(line, "next-hop") else None
				if str(subnet) != str(prev_route):
					if routes.get(subnet_header):
						attribute = routes[subnet_header]
						if next_hop:
							if attribute.get('next_hop'):
								msr = self.matching_static_route(routes, subnet_header)
								if msr: new_subnet_header = subnet_header + "_" + str(msr)
								routes[new_subnet_header] = dict(routes[subnet_header])
								attribute = routes[new_subnet_header]
							attribute.update({'next_hop': next_hop})
					else:
						routes[subnet_header] = {'subnet': subnet}
						attribute = routes[subnet_header]
						if next_hop: attribute.update({'next_hop': next_hop})
						subnet_header = subnet
				if vrf: attribute.update({'vrf': vrf})
				if tag: attribute.update({'tag': tag})
		return routes


	""" OSPF """

	def ospf_all(self):
		"""ospf facts"""
		ospf = {'global': {}}
		for line in self.run_list:
			if not STR.found(line, "protocols ospf"): continue
			spl = line.split()
			vrf = spl[2] if spl[1] == 'routing-instances' else 'global'
			if not ospf.get(vrf): 
				ospf[vrf] = {}
				ospf_instance = ospf[vrf]
				ospf_instance['instance'] = vrf
			if 'area' in spl:
				area_idx = spl.index('area') + 1
				area = "area_" + spl[area_idx]
				if not ospf_instance.get(area): ospf_instance[area] = {}				
				area_of_instance = ospf_instance[area]
				if 'area-range' in spl:
					arearange_idx = spl.index('area-range') + 1
					area_summary = spl[arearange_idx]
					if not ospf_instance.get('area_summaries'): area_of_instance['area_summaries'] = []
					area_summaries = area_of_instance['area_summaries']
					area_summaries.append(spl[arearange_idx])

		return ospf

	""" BGP """

	def bgp_all(self):
		"""bgp facts"""
		bgp = {'global': {}}
		for line in self.run_list:
			if STR.found(line, "autonomous-system"):
				spl = line.split()
				for _ in spl:
					if _.isdigit(): 
						bgp['AS'] = int(_)
						break
				continue
			if not STR.found(line, "protocols bgp"): continue
			spl = line.split()
			vrf = spl[2] if spl[1] == 'routing-instances' else 'global'
			if not bgp.get(vrf): 
				bgp[vrf] = {'peer_group': {}}
				bgp_instance = bgp[vrf]
				pg = bgp_instance['peer_group']
			if STR.found(line, 'group'):
				group_idx = spl.index('group') + 1
				if not pg.get(spl[group_idx]): pg[spl[group_idx]] = {}

				if STR.found(line, 'neighbor'):
					nbr_idx = spl.index('neighbor') + 1
					pg[spl[group_idx]][spl[nbr_idx]] = {}
					peer_grp = pg[spl[group_idx]][spl[nbr_idx]]
				else:
					peer_grp = pg[spl[group_idx]]

				if STR.found(line, 'description'):
					desc_idx = spl.index('description') + 1
					peer_grp['description'] = " ".join(spl[desc_idx:])
				if STR.found(line, 'peer-as'):
					peeras_idx = spl.index('peer-as') + 1
					peer_grp['peer_as'] = int(spl[peeras_idx])
				if STR.found(line, 'local-as'):
					localas_idx = spl.index('local-as') + 1
					peer_grp['local_as'] = int(spl[localas_idx])
				if STR.found(line, 'local-address'):
					localadd_idx = spl.index('local-address') + 1
					peer_grp['local_address'] = IPv4(spl[localadd_idx]+"/32")
				if STR.found(line, 'type'):
					neighbor_type = 'ibgp' if spl[-1] == 'internal' else 'ebgp'
					peer_grp['neighbor_type'] = neighbor_type

		return bgp



# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
	pass
# ---------------------------------------------------------------------------- #
