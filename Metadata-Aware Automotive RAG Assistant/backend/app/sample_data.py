"""
Drive Wise - Sample Brochure Data
Realistic demo data for Hyundai Creta, Tata Nexon, and Maruti Suzuki Brezza.
Used to populate the vector store when no PDF brochures have been uploaded.
"""

SAMPLE_BROCHURES = {
    "Hyundai": {
        "Creta": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 4,
                    "content": (
                        "The Hyundai Creta 2024 is available with three sophisticated engine options "
                        "designed to deliver an optimal balance of power, efficiency, and driving pleasure. "
                        "The 1.5L MPi Petrol Engine produces 115 PS of maximum power at 6,300 rpm and "
                        "144 Nm of peak torque at 4,500 rpm. It is paired with either a 6-speed manual "
                        "transmission or an Intelligent Variable Transmission (IVT) for seamless acceleration. "
                        "The 1.5L U2 CRDi Diesel Engine delivers 116 PS of power at 4,000 rpm and an "
                        "impressive 250 Nm of torque at 1,500-2,750 rpm, making it ideal for highway cruising "
                        "and long-distance travel. It comes with a 6-speed manual or a 6-speed automatic transmission. "
                        "For enthusiasts seeking sporty performance, the 1.5L Turbo GDi Petrol Engine generates "
                        "160 PS at 5,500 rpm and 253 Nm at 1,500-3,500 rpm, paired with a 7-speed DCT "
                        "(Dual Clutch Transmission) for lightning-fast gear shifts. "
                        "All engines feature Drive Mode Select with Eco, Normal, and Sport modes, allowing "
                        "drivers to customize the driving experience. The Creta also features a well-tuned "
                        "McPherson Strut front suspension and Coupled Torsion Beam Axle rear suspension for "
                        "a comfortable yet responsive ride quality."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 6,
                    "content": (
                        "The Hyundai Creta 2024 delivers outstanding fuel efficiency across all its powertrain options. "
                        "The 1.5L MPi Petrol engine with manual transmission achieves an ARAI-certified mileage of "
                        "17.4 km/l, while the IVT variant returns 17.0 km/l. The 1.5L Diesel engine leads the "
                        "segment with an exceptional 21.8 km/l with manual transmission and 18.5 km/l with the "
                        "automatic transmission. The 1.5L Turbo GDi Petrol with 7-speed DCT delivers 18.4 km/l. "
                        "The Creta features an Eco driving mode that optimizes throttle response, transmission "
                        "shift points, and air conditioning compressor operation to maximize fuel savings during "
                        "city driving. The idle start/stop system further improves efficiency by automatically "
                        "shutting off the engine at traffic signals and restarting it when the clutch is pressed. "
                        "The fuel tank capacity is 50 liters across all variants, providing a range of approximately "
                        "870-1,090 km on a full tank depending on the engine variant and driving conditions."
                    )
                },
                "Safety Features": {
                    "page": 8,
                    "content": (
                        "The Hyundai Creta 2024 prioritizes occupant safety with a comprehensive suite of active "
                        "and passive safety features. It comes equipped with 6 airbags as standard across all "
                        "variants, including dual front airbags, front side airbags, and curtain airbags. "
                        "Active safety features include Electronic Stability Control (ESC), Vehicle Stability "
                        "Management (VSM), Hill-start Assist Control (HAC), and Brake Assist System (BAS). "
                        "The Anti-lock Braking System (ABS) with Electronic Brakeforce Distribution (EBD) ensures "
                        "controlled braking in all conditions. The Creta also features a Tyre Pressure Monitoring "
                        "System (TPMS), ISOFIX child seat anchors, rear parking sensors, and a reverse parking "
                        "camera with dynamic guidelines. Higher variants add a 360-degree camera system with "
                        "Blind-Spot Collision-Avoidance Assist (BCA), Rear Cross-Traffic Collision-Avoidance "
                        "Assist (RCCA), and Forward Collision-Avoidance Assist (FCA) with pedestrian detection. "
                        "The high-strength steel body structure with advanced crumple zones ensures maximum "
                        "protection during collisions. The Creta has received a 5-star safety rating from "
                        "Global NCAP, demonstrating its commitment to occupant safety."
                    )
                },
                "Dimensions & Space": {
                    "page": 10,
                    "content": (
                        "The Hyundai Creta 2024 offers a spacious and well-proportioned cabin within its compact "
                        "SUV dimensions. The overall length is 4,330 mm, width is 1,790 mm, and height is 1,635 mm, "
                        "providing a commanding road presence. The wheelbase measures 2,610 mm, resulting in "
                        "generous rear legroom and cabin space. The ground clearance stands at 190 mm, suitable "
                        "for Indian road conditions including speed breakers and unpaved surfaces. "
                        "The boot space is a class-leading 433 liters, expandable with the 60:40 split-folding "
                        "rear seats for larger cargo requirements. The kerb weight ranges from 1,210 kg to "
                        "1,380 kg depending on the variant and engine option. The turning radius is 5.2 meters, "
                        "making city maneuvering and parking effortless. Interior headroom is 1,000 mm in the "
                        "front and 975 mm in the rear, ensuring comfortable seating for tall occupants."
                    )
                },
                "Interior & Comfort": {
                    "page": 12,
                    "content": (
                        "The Hyundai Creta 2024 interior features a premium dual-tone cabin with soft-touch "
                        "materials and ambient lighting creating a luxurious atmosphere. The driver-centric cockpit "
                        "features a 10.25-inch HD touchscreen infotainment display seamlessly integrated with a "
                        "10.25-inch fully digital instrument cluster, creating a connected panoramic display. "
                        "Comfort highlights include ventilated front seats with 8-way power adjustment for the "
                        "driver, a panoramic sunroof with electric sunblind, automatic climate control with "
                        "rear AC vents, leather-wrapped steering wheel with mounted controls, and push-button "
                        "start with smart key. The rear seats feature adjustable headrests, center armrest "
                        "with cupholders, and USB charging ports. The cabin also features a wireless phone "
                        "charger, air purifier with AQI display, sunglass holder, and an electric parking brake "
                        "with auto hold function. The Bose premium sound system with 8 speakers delivers "
                        "exceptional audio quality throughout the cabin."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 14,
                    "content": (
                        "The Hyundai Creta 2024 comes equipped with a state-of-the-art infotainment system "
                        "centered around the 10.25-inch HD touchscreen with split-screen functionality. "
                        "It supports wireless Android Auto and Apple CarPlay for seamless smartphone integration. "
                        "The Hyundai Bluelink connected car technology offers over 60 connected features including "
                        "remote engine start/stop, remote climate control, remote door lock/unlock, vehicle "
                        "status monitoring, SOS emergency assistance, and geo-fence alerts. "
                        "Voice commands powered by Hyundai's intelligent voice recognition allow hands-free "
                        "control of navigation, climate, and media functions. The system includes built-in "
                        "navigation with real-time traffic updates, Bluetooth multi-connectivity for two phones "
                        "simultaneously, and support for Indian regional languages. "
                        "The Bose premium 8-speaker sound system features a subwoofer and amplifier for "
                        "immersive audio. Additional connectivity includes USB-C charging ports, a wireless "
                        "phone charger, and a dedicated Hyundai Bluelink smartphone app for remote vehicle "
                        "management. OTA (Over-The-Air) map and software updates keep the system current."
                    )
                },
                "Exterior Design": {
                    "page": 16,
                    "content": (
                        "The Hyundai Creta 2024 showcases a bold and dynamic exterior design language that "
                        "reflects its premium positioning. The front fascia features the signature Parametric "
                        "Jewel Pattern grille with integrated LED positioning lights, flanked by full LED "
                        "projector headlamps with Sequential Turn Indicators. The muscular bonnet with "
                        "prominent character lines flows into the sculpted sides with a bold shoulder line. "
                        "The side profile highlights R17 diamond-cut alloy wheels, chrome door handles, "
                        "and integrated roof rails. The rear features connected LED tail lamps spanning "
                        "the width of the vehicle, a rear spoiler, and dual-tone skid plates. "
                        "The Creta is available in 8 exterior color options including Abyss Black, Atlas White, "
                        "Titan Grey, Fiery Red, Robust Emerald, and three dual-tone combinations with a "
                        "contrasting Phantom Black roof. The dual-tone option adds a sportier visual appeal."
                    )
                },
                "Warranty & Service": {
                    "page": 18,
                    "content": (
                        "The Hyundai Creta 2024 comes with a comprehensive 3-year/unlimited kilometer warranty "
                        "as standard, providing peace of mind to owners. Extended warranty plans of up to 5 years "
                        "are available for additional coverage. Hyundai also offers a 3-year roadside assistance "
                        "program covering battery jump-start, flat tyre change, emergency fuel delivery, towing, "
                        "and on-spot minor repairs. The service network spans over 1,500 authorized service "
                        "centers across India, ensuring convenient access to maintenance and repairs. "
                        "Hyundai offers transparent service pricing through its 'Click to Buy' online platform "
                        "and genuine spare parts availability. Scheduled service intervals are every 10,000 km "
                        "or 1 year, whichever comes first. The annual maintenance cost for the petrol variant "
                        "is approximately Rs. 4,500-5,500, and for the diesel variant, approximately Rs. 5,500-7,000. "
                        "Hyundai also provides a free first service within 1,000 km or 1 month of purchase."
                    )
                }
            }
        },
        "Venue": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 4,
                    "content": (
                        "The Hyundai Venue 2024 offers two engine options tailored for urban commuters and "
                        "enthusiasts alike. The 1.2L Kappa Petrol Engine produces 83 PS of power at 6,000 rpm "
                        "and 114 Nm of torque at 4,000 rpm, paired with a 5-speed manual transmission for "
                        "efficient city driving. The 1.0L Turbo GDi Petrol Engine delivers a spirited 120 PS "
                        "at 6,000 rpm and 172 Nm of torque at 1,500-4,000 rpm, available with either a "
                        "6-speed iMT (intelligent Manual Transmission) or a 7-speed DCT for a sportier "
                        "driving experience. Both engines feature refined NVH characteristics for a quiet "
                        "cabin experience and responsive throttle mapping for confident overtaking."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 6,
                    "content": (
                        "The Hyundai Venue 2024 is designed for excellent fuel economy. The 1.2L Kappa Petrol "
                        "engine achieves 17.5 km/l (ARAI certified). The 1.0L Turbo GDi with iMT delivers "
                        "18.1 km/l, and the DCT variant returns 18.0 km/l. The Venue features Eco, Normal, "
                        "and Sport drive modes to optimize fuel consumption based on driving conditions. "
                        "The fuel tank capacity is 45 liters, providing an estimated range of 787-815 km."
                    )
                },
                "Safety Features": {
                    "page": 8,
                    "content": (
                        "The Hyundai Venue 2024 offers 6 airbags as standard, ESC, VSM, Hill Assist, ABS with "
                        "EBD, rear parking camera with guidelines, TPMS, ISOFIX child seat mounts, and a "
                        "high-strength steel body. Higher trims include Blind-Spot Collision Warning and "
                        "Rear Cross-Traffic Alert for enhanced urban safety."
                    )
                },
                "Dimensions & Space": {
                    "page": 10,
                    "content": (
                        "The Hyundai Venue 2024 is a sub-4-meter compact SUV measuring 3,995 mm in length, "
                        "1,770 mm in width, and 1,617 mm in height. The wheelbase is 2,500 mm providing "
                        "adequate legroom. Ground clearance is 190 mm, and boot space is 350 liters. "
                        "The turning radius of 5.2 meters makes it highly maneuverable in tight spaces."
                    )
                },
                "Interior & Comfort": {
                    "page": 12,
                    "content": (
                        "The Venue interior features an 8-inch touchscreen, automatic climate control, "
                        "wireless phone charger, push-button start, rear AC vents, height-adjustable "
                        "driver seat, and a leather-wrapped steering wheel with audio and telephony controls."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 14,
                    "content": (
                        "The Venue offers an 8-inch HD touchscreen with wireless Android Auto and Apple CarPlay. "
                        "Bluelink connected car features include over 60 functions such as remote engine start, "
                        "vehicle tracking, SOS, geo-fence, and AI-based voice recognition supporting natural "
                        "language commands in Indian English and Hindi."
                    )
                },
                "Exterior Design": {
                    "page": 16,
                    "content": (
                        "The Venue 2024 features a bold front with a dark chrome parametric grille, LED "
                        "projector headlamps, LED DRLs with sequential turn signals, R16 diamond-cut alloy "
                        "wheels, roof rails, and connected LED tail lamps. Available in 7 monotone and "
                        "3 dual-tone color options."
                    )
                },
                "Warranty & Service": {
                    "page": 18,
                    "content": (
                        "The Venue comes with a 3-year/unlimited km warranty, extendable to 5 years. "
                        "3-year roadside assistance is included. Service intervals are every 10,000 km. "
                        "Annual maintenance costs are approximately Rs. 3,500-5,000."
                    )
                }
            }
        }
    },
    "Tata": {
        "Nexon": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 5,
                    "content": (
                        "The Tata Nexon 2024 is powered by two refined engine options engineered for Indian "
                        "driving conditions. The 1.2L Revotron Turbocharged Petrol Engine generates 120 PS of "
                        "maximum power at 5,500 rpm and 170 Nm of peak torque at 1,750-4,000 rpm, providing "
                        "strong mid-range performance for city and highway driving. It is available with a "
                        "6-speed manual transmission or a 6-speed AMT (Automated Manual Transmission). "
                        "The 1.5L Revotorq Turbocharged Diesel Engine delivers 115 PS of power at 4,000 rpm "
                        "and an impressive 260 Nm of torque at 1,500-2,750 rpm, offering exceptional pulling "
                        "power and highway cruising capability. The diesel engine is available with a 6-speed "
                        "manual or 6-speed AMT. Both engines feature Multi-drive modes including Eco, City, "
                        "and Sport, allowing drivers to adapt the car's behavior to their driving style. "
                        "The Nexon's suspension setup includes an Independent McPherson Strut with coil spring "
                        "at the front and a Semi-Independent Twist Beam with coil spring at the rear, "
                        "delivering a comfortable yet engaging ride quality."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 7,
                    "content": (
                        "The Tata Nexon 2024 delivers impressive fuel efficiency across both powertrain options. "
                        "The 1.2L Turbocharged Petrol engine achieves 17.4 km/l with the manual transmission "
                        "and 17.0 km/l with the AMT (ARAI certified). The 1.5L Turbocharged Diesel engine "
                        "delivers an outstanding 24.1 km/l with the manual and 22.1 km/l with the AMT, making "
                        "it one of the most fuel-efficient compact SUVs in India. "
                        "The Eco drive mode optimizes engine response and gear shift patterns to maximize fuel "
                        "economy during city driving. The idle start-stop feature further enhances efficiency by "
                        "automatically turning off the engine at traffic stops. The fuel tank capacity is "
                        "44 liters, offering a range of approximately 766-1,060 km depending on the variant "
                        "and driving conditions."
                    )
                },
                "Safety Features": {
                    "page": 9,
                    "content": (
                        "The Tata Nexon 2024 is India's first compact SUV to achieve a 5-star Global NCAP "
                        "safety rating, demonstrating Tata's unwavering commitment to vehicle safety. "
                        "The Nexon features 6 airbags as standard across all variants, including dual front "
                        "airbags, front side airbags, and curtain airbags for comprehensive protection. "
                        "Active safety systems include Electronic Stability Program (ESP) with rollover "
                        "mitigation, Anti-lock Braking System (ABS) with Electronic Brakeforce Distribution "
                        "(EBD), Corner Stability Control (CSC), Hill Hold Control (HHC), and Traction Control. "
                        "The Nexon also features a 360-degree surround view camera system, rear parking sensors, "
                        "a Tyre Pressure Monitoring System (TPMS), ISOFIX child seat anchors, and speed-sensing "
                        "automatic door locks. The OMEGA (Optimal Modular Efficient Global Advanced) architecture "
                        "features impact-absorbing crumple zones, side impact beams, and reinforced passenger "
                        "cell for maximum occupant protection. Rain-sensing wipers and auto headlamps add to "
                        "the safety convenience features."
                    )
                },
                "Dimensions & Space": {
                    "page": 11,
                    "content": (
                        "The Tata Nexon 2024 is a sub-4-meter compact SUV with dimensions optimized for urban "
                        "agility while maximizing interior space. The overall length is 3,993 mm, width is "
                        "1,811 mm, and height is 1,606 mm. The wide body gives the Nexon a planted stance "
                        "while the compact length makes it easy to navigate through city traffic. "
                        "The wheelbase of 2,498 mm provides adequate legroom for rear passengers. Ground "
                        "clearance is 209 mm (unladen), one of the highest in its segment, ensuring excellent "
                        "ability to tackle rough roads and deep potholes. The boot space is 382 liters with "
                        "the rear seats up, expandable by folding the 60:40 split rear seats. "
                        "The kerb weight ranges from 1,240 kg to 1,365 kg across variants. The turning radius "
                        "is 5.3 meters."
                    )
                },
                "Interior & Comfort": {
                    "page": 13,
                    "content": (
                        "The Tata Nexon 2024 features a premium Chromatic Ivory and Ash Wood interior theme "
                        "with soft-touch dashboard materials. The cabin is centered around a 10.25-inch floating "
                        "HD touchscreen infotainment display positioned for optimal driver visibility. "
                        "Comfort features include automatic climate control with rear AC vents, ventilated "
                        "leatherette front seats, 6-way electrically adjustable driver seat, push-button start "
                        "with proximity key, cooled glove box, height-adjustable front seatbelts, and a "
                        "leather-wrapped flat-bottom steering wheel with illuminated controls. "
                        "The electric sunroof with anti-pinch function lets in natural light for an airy feel. "
                        "The Nexon also features an air purifier with AQI display, ambient mood lighting with "
                        "customizable colors, rear center armrest with cupholders, and 45-liter cooled storage. "
                        "The 7-inch TFT instrument cluster displays comprehensive vehicle information including "
                        "turn-by-turn navigation, drive mode, and safety alerts."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 15,
                    "content": (
                        "The Tata Nexon 2024 infotainment system features a 10.25-inch floating HD touchscreen "
                        "running on a responsive quad-core processor. It supports wireless Android Auto and "
                        "wireless Apple CarPlay for seamless smartphone connectivity. "
                        "The Harman premium sound system with 9 speakers (including a subwoofer and amplifier) "
                        "delivers immersive audio quality. The iRA (Intelligent Real-time Assist) connected car "
                        "platform offers over 45 connected features including remote vehicle control, vehicle "
                        "health monitoring, SOS emergency assist, geo-fence alerts, trip analytics, and voice "
                        "assistant powered by Alexa. The system supports OTA (Over-The-Air) updates for maps "
                        "and software. Additional connectivity features include 2 USB-C fast charging ports, "
                        "a wireless phone charger, and Bluetooth 5.0 for stable audio streaming."
                    )
                },
                "Exterior Design": {
                    "page": 17,
                    "content": (
                        "The Tata Nexon 2024 features the IMPACT 2.0 design language with a bold and aggressive "
                        "exterior. The front fascia showcases the Humanity Line with a digital hexagonal grille "
                        "flanked by full LED projector headlamps with LED DRLs and sequential turn indicators. "
                        "The side profile highlights the coupe-like roofline, flared wheel arches housing "
                        "R16 diamond-cut dual-tone alloy wheels, body-colored door handles, and chrome "
                        "window line. The rear features distinctive LED pilot lamps connected by an LED light "
                        "bar, sporty rear spoiler, and sculpted bumper with dual-tone skid plate. "
                        "The Nexon is available in 10 color options including Fearless Purple, Flame Red, "
                        "Creative Ocean, Daytona Grey, and 5 dual-tone combinations with a contrasting "
                        "Midnight Black or Pristine White roof."
                    )
                },
                "Warranty & Service": {
                    "page": 19,
                    "content": (
                        "The Tata Nexon 2024 comes with a standard 2-year/75,000 km warranty, which can be "
                        "extended up to 5 years/1,50,000 km with Tata's extended warranty packages. "
                        "Tata Motors offers a 24/7 roadside assistance program for emergency support. "
                        "The service network includes over 1,100 authorized service centers across India. "
                        "Service intervals are every 15,000 km or 1 year, whichever comes first. "
                        "The annual maintenance cost ranges from Rs. 5,000-7,000 for petrol and Rs. 6,000-8,500 "
                        "for diesel variants. Tata also offers prepaid service packages and transparent pricing "
                        "through its service cost calculator on the official website."
                    )
                }
            }
        }
    },
    "Maruti Suzuki": {
        "Brezza": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 4,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 is powered by a next-generation 1.5L K15C DualJet "
                        "Petrol Engine with Progressive Smart Hybrid technology. This advanced powertrain "
                        "produces 103 PS of maximum power at 6,000 rpm and 137 Nm of peak torque at 4,400 rpm. "
                        "The engine features dual injectors per cylinder and a cooled EGR (Exhaust Gas "
                        "Recirculation) system for improved combustion efficiency. "
                        "Transmission options include a slick 5-speed manual gearbox and a 6-speed torque "
                        "converter automatic transmission with paddle shifters for an engaging drive. "
                        "The Smart Hybrid system utilizes an Integrated Starter Generator (ISG) and lithium-ion "
                        "battery to provide electric assist during acceleration, idle start-stop, and energy "
                        "regeneration during braking. The Brezza features a well-tuned McPherson Strut front "
                        "suspension and Torsion Beam rear suspension for a balanced ride-handling combination."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 6,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 delivers class-leading fuel efficiency thanks to its "
                        "Smart Hybrid technology. The manual transmission variant achieves an ARAI-certified "
                        "mileage of 25.51 km/l, while the automatic variant returns 19.80 km/l. "
                        "The Progressive Smart Hybrid system contributes to fuel savings through idle start-stop, "
                        "torque assist during acceleration, and regenerative braking that recovers energy. "
                        "The fuel tank capacity is 48 liters, providing an estimated range of 950-1,225 km "
                        "on a full tank depending on the transmission variant. "
                        "The Brezza's lightweight Heartect platform contributes to its excellent fuel economy "
                        "while maintaining structural rigidity. Real-world mileage typically ranges from "
                        "15-18 km/l in city conditions and 19-22 km/l on highways."
                    )
                },
                "Safety Features": {
                    "page": 8,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 offers a comprehensive safety package built on the "
                        "rigid Heartect platform. Standard safety features across all variants include 6 airbags "
                        "(dual front, side, and curtain), ESP (Electronic Stability Program) with hill hold, "
                        "ABS with EBD, brake assist, rear parking camera with sensors, ISOFIX child seat "
                        "anchors, seat belt reminder for all seats, and speed alert system. "
                        "Higher variants add a 360-degree camera view, Head-Up Display (HUD) projecting speed "
                        "and navigation on the windshield, and Suzuki Connect telematics with emergency SOS. "
                        "The Heartect platform uses high-tensile steel at critical junctions and features "
                        "energy-absorbing structures for frontal, side, and rear impact protection. "
                        "The Brezza has achieved a 4-star Global NCAP safety rating."
                    )
                },
                "Dimensions & Space": {
                    "page": 10,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 is a sub-4-meter compact SUV measuring 3,995 mm in "
                        "length, 1,790 mm in width, and 1,640 mm in height. The wheelbase of 2,500 mm ensures "
                        "generous legroom for rear passengers. Ground clearance is 198 mm, providing excellent "
                        "ability to navigate over speed breakers and rough terrain. "
                        "The boot space is 328 liters with rear seats up, expandable by folding the 60:40 "
                        "split rear seats. The kerb weight ranges from 1,095 kg to 1,185 kg, making it one of "
                        "the lightest SUVs in the segment, which contributes to its agile handling and fuel "
                        "efficiency. The turning radius is 5.2 meters for easy city maneuvering."
                    )
                },
                "Interior & Comfort": {
                    "page": 12,
                    "content": (
                        "The Brezza 2024 interior features a dual-tone black and brown theme with a layered "
                        "dashboard design. The cabin is highlighted by a 9-inch SmartPlay Pro+ touchscreen "
                        "infotainment system positioned at the center. Comfort features include an electric "
                        "sunroof, automatic climate control, cruise control, push-button start with smart key, "
                        "leather-wrapped steering wheel with audio and call controls, height-adjustable "
                        "driver seat, and 60:40 split-folding rear seats with reclining function. "
                        "The Brezza also offers a wireless phone charger, USB-C charging ports for both rows, "
                        "rear AC vents, adjustable rear headrests, and an integrated armrest with storage. "
                        "The Head-Up Display (HUD) in top variants projects essential driving information "
                        "onto the windshield, allowing the driver to keep their eyes on the road."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 14,
                    "content": (
                        "The Brezza 2024 comes with a 9-inch SmartPlay Pro+ touchscreen infotainment system "
                        "with wireless Apple CarPlay and Android Auto. The Arkamys-tuned sound system with "
                        "6 speakers delivers rich and balanced audio. The Suzuki Connect telematics platform "
                        "offers over 40 connected features including vehicle tracking, driving behavior "
                        "analysis, trip history, safety alerts, and remote AC control. "
                        "The system includes built-in navigation, voice recognition for hands-free operation, "
                        "and Bluetooth connectivity. Additional features include a USB-C fast charging port, "
                        "steering-mounted audio controls, and smartphone app integration for remote vehicle "
                        "monitoring. The Head-Up Display adds another layer of connectivity by showing "
                        "phone notifications and navigation directions directly in the driver's line of sight."
                    )
                },
                "Exterior Design": {
                    "page": 16,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 features a neo-futuristic exterior design with a bold "
                        "front grille, LED projector headlamps with integrated LED DRLs, and a chrome-accented "
                        "front bumper. The side profile showcases R16 precision-cut dual-tone alloy wheels, "
                        "body-colored door handles, side turn indicator on ORVMs, and roof rails. "
                        "The rear features wraparound LED tail lamps, a rear spoiler, and a skid plate. "
                        "The Brezza is available in 9 monotone and 3 dual-tone color options including "
                        "Sizzling Red, Pearl Arctic White, Brave Khaki, Splendid Silver, and dual-tone "
                        "combinations with a Midnight Black roof."
                    )
                },
                "Warranty & Service": {
                    "page": 18,
                    "content": (
                        "The Maruti Suzuki Brezza 2024 comes with a standard 2-year/40,000 km warranty, "
                        "extendable up to 5 years. Maruti Suzuki boasts the largest service network in India "
                        "with over 4,600 authorized service centers across the country. Service intervals "
                        "are every 10,000 km or 1 year, whichever comes first. The annual maintenance cost "
                        "is approximately Rs. 3,500-5,000, making it one of the most affordable SUVs to "
                        "maintain. Maruti offers prepaid service plans, genuine parts guarantee, and 24/7 "
                        "roadside assistance through its RSA program."
                    )
                }
            }
        },
        "Grand Vitara": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 4,
                    "content": (
                        "The Maruti Suzuki Grand Vitara 2024 offers two advanced powertrain options. The 1.5L "
                        "K15C DualJet Smart Hybrid engine produces 103 PS and 137 Nm, available with 5-speed MT "
                        "or 6-speed AT. The 1.5L Intelligent Electric Hybrid with e-CVT generates a combined "
                        "116 PS, featuring three driving modes: EV, Eco, and Power. The strong hybrid system "
                        "can run on pure electric power at low speeds for up to 40% of driving time in city "
                        "conditions, significantly reducing fuel consumption and emissions."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 6,
                    "content": (
                        "The Grand Vitara delivers exceptional fuel economy. The Smart Hybrid MT variant achieves "
                        "21.11 km/l, the AT variant returns 20.58 km/l, and the Strong Hybrid variant achieves a "
                        "class-leading 27.97 km/l (ARAI certified), making it the most fuel-efficient SUV in "
                        "India. The strong hybrid's regenerative braking and EV mode contribute to real-world "
                        "savings of up to 40% over conventional petrol engines."
                    )
                },
                "Safety Features": {
                    "page": 8,
                    "content": (
                        "The Grand Vitara features 6 airbags, ESP, hill hold, ABS with EBD, 360-degree camera, "
                        "Head-Up Display, TPMS, ISOFIX, rear parking sensors, and a high-strength Heartect-II "
                        "platform. It also offers Suzuki Connect with emergency SOS and real-time vehicle "
                        "tracking. The ALLGRIP AWD system in select variants provides enhanced traction "
                        "in Snow, Mud, Sand, and Lock modes."
                    )
                },
                "Dimensions & Space": {
                    "page": 10,
                    "content": (
                        "The Grand Vitara measures 4,345 mm in length, 1,795 mm in width, and 1,645 mm in "
                        "height with a 2,600 mm wheelbase. Ground clearance is 210 mm for excellent off-road "
                        "capability. Boot space is 373 liters with a flat loading floor. Kerb weight ranges "
                        "from 1,165-1,290 kg."
                    )
                },
                "Interior & Comfort": {
                    "page": 12,
                    "content": (
                        "The Grand Vitara interior features a premium cabin with a 9-inch SmartPlay Pro+ "
                        "touchscreen, panoramic sunroof, ventilated front seats, wireless charger, Head-Up "
                        "Display, automatic climate control, push-button start, and ambient mood lighting. "
                        "The cabin uses soft-touch materials with silver accents throughout."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 14,
                    "content": (
                        "The Grand Vitara features a 9-inch SmartPlay Pro+ touchscreen with wireless Android "
                        "Auto and Apple CarPlay, Arkamys-tuned 6-speaker audio, Suzuki Connect with 40+ "
                        "connected features, voice recognition, built-in navigation, and USB-C fast charging."
                    )
                },
                "Exterior Design": {
                    "page": 16,
                    "content": (
                        "The Grand Vitara features a chrome-accented 3-slat front grille, LED projector headlamps "
                        "with sequential DRLs, R17 dual-tone alloy wheels, integrated roof rails, and "
                        "LED tail lamps. Available in 8 monotone and 3 dual-tone options."
                    )
                },
                "Warranty & Service": {
                    "page": 18,
                    "content": (
                        "Standard 3-year/100,000 km warranty (extendable to 5 years), 24/7 RSA, 4,600+ service "
                        "centers across India. The hybrid battery carries an 8-year/160,000 km warranty. "
                        "Annual service costs are Rs. 4,000-6,000."
                    )
                }
            }
        }
    },
    "Mahindra": {
        "XUV700": {
            "document_version": "2024 Edition",
            "sections": {
                "Engine & Performance": {
                    "page": 5,
                    "content": (
                        "The Mahindra XUV700 2024 is available with two powerful mStallion engine options. "
                        "The 2.0L mStallion Turbo Petrol Engine produces a class-leading 200 PS of power at "
                        "5,000 rpm and 380 Nm of torque at 1,750-3,000 rpm, making it the most powerful engine "
                        "in the segment. The 2.2L mHawk Diesel Engine delivers 185 PS of power at 3,500 rpm "
                        "and a massive 420 Nm (MT) / 450 Nm (AT) of torque at 1,750-2,800 rpm. "
                        "Both engines are available with a 6-speed manual transmission or a 6-speed torque "
                        "converter automatic. The diesel AT variant is also available with an optional "
                        "AWD (All-Wheel Drive) system with multiple terrain modes for off-road capability. "
                        "Drive modes include Zip (Eco), Zap (Normal), and Zoom (Sport) for customizable "
                        "driving dynamics."
                    )
                },
                "Mileage & Fuel Efficiency": {
                    "page": 7,
                    "content": (
                        "The XUV700 delivers competitive fuel efficiency for its size and power output. "
                        "The 2.0L Turbo Petrol achieves 16.0 km/l (MT) and 15.2 km/l (AT). The 2.2L Diesel "
                        "delivers an impressive 18.0 km/l (MT) and 16.3 km/l (AT). The AWD diesel variant "
                        "returns 14.5 km/l. Fuel tank capacity is 60 liters, providing a range of up to "
                        "1,080 km with the diesel manual variant."
                    )
                },
                "Safety Features": {
                    "page": 9,
                    "content": (
                        "The XUV700 offers a class-leading safety package with 7 airbags (including a knee "
                        "airbag), ADAS Level 2 features including Adaptive Cruise Control, Forward Collision "
                        "Warning, Autonomous Emergency Braking, Lane Keep Assist, Lane Departure Warning, "
                        "High Beam Assist, and Traffic Sign Recognition. Additional features include ESP, "
                        "Hill Hold/Descent Control, 360-degree camera, front parking sensors, TPMS, electronic "
                        "parking brake, driver drowsiness detection, and a reinforced body structure. "
                        "The XUV700 has received a 5-star Global NCAP safety rating with the highest score "
                        "ever for an Indian car."
                    )
                },
                "Dimensions & Space": {
                    "page": 11,
                    "content": (
                        "The XUV700 measures 4,695 mm in length, 1,890 mm in width, and 1,755 mm in height "
                        "with a 2,750 mm wheelbase. Available in both 5-seater and 7-seater configurations. "
                        "Ground clearance is 200 mm. Boot space is 451 liters (5-seat) or 239 liters (7-seat "
                        "with third row up). The third-row seats offer adequate space for adults on short trips."
                    )
                },
                "Interior & Comfort": {
                    "page": 13,
                    "content": (
                        "The XUV700 interior features dual 10.25-inch screens (infotainment + instrument cluster), "
                        "a panoramic skyroof, Alexa voice assistant, Sony 3D surround sound system with 12 "
                        "speakers, wireless charging, dual-zone climate control, ventilated and electrically "
                        "adjustable front seats, 64-color ambient lighting, electronic parking brake with auto "
                        "hold, and a flat-bottom leather steering wheel. Smart Door Handles that flush with the "
                        "body deploy on approach."
                    )
                },
                "Infotainment & Connectivity": {
                    "page": 15,
                    "content": (
                        "The XUV700 features a 10.25-inch AdrenoX infotainment system with wireless Android Auto "
                        "and Apple CarPlay, built-in Alexa, Sony 3D surround sound with 12 speakers, "
                        "AdrenoX connected car features with over 60 functions, dual-SIM connectivity, "
                        "OTA updates, and smart watch integration. The system runs on a Qualcomm Snapdragon "
                        "processor for smooth performance."
                    )
                },
                "Exterior Design": {
                    "page": 17,
                    "content": (
                        "The XUV700 features Mahindra's Twin Peaks logo, a bold chrome grille, C-shaped LED "
                        "DRLs with sequential indicators, LED projector headlamps, R18 diamond-cut alloy "
                        "wheels, flush door handles, a panoramic sunroof, and connected LED tail lamps. "
                        "Available in 7 color options."
                    )
                },
                "Warranty & Service": {
                    "page": 19,
                    "content": (
                        "The XUV700 comes with a 3-year/100,000 km warranty, extendable up to 7 years. "
                        "Mahindra offers 24/7 roadside assistance and has over 400 service centers across India. "
                        "Service intervals are every 10,000 km or 1 year. Annual maintenance costs range from "
                        "Rs. 6,000-9,000 depending on the variant."
                    )
                }
            }
        }
    }
}


def get_all_chunks():
    """
    Convert the sample brochure data into a flat list of chunks 
    with metadata, ready for vector store ingestion.
    """
    chunks = []
    for brand, models in SAMPLE_BROCHURES.items():
        for model_name, model_data in models.items():
            doc_version = model_data["document_version"]
            for section_name, section_data in model_data["sections"].items():
                chunk = {
                    "text": section_data["content"],
                    "metadata": {
                        "brand": brand,
                        "model": model_name,
                        "section": section_name,
                        "page_number": section_data["page"],
                        "document_version": doc_version,
                        "brochure_name": f"{brand} {model_name} Brochure - {doc_version}",
                        "source": "sample_data"
                    }
                }
                chunks.append(chunk)
    return chunks


def get_available_brands():
    """Return list of all available car brands."""
    return sorted(SAMPLE_BROCHURES.keys())


def get_models_for_brand(brand: str):
    """Return list of available models for a given brand."""
    if brand in SAMPLE_BROCHURES:
        return sorted(SAMPLE_BROCHURES[brand].keys())
    return []
